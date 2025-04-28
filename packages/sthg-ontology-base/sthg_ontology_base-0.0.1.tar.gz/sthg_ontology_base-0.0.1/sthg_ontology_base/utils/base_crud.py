
from typing import TypeVar, Generic, Type, Any, List, Optional, Union

from sqlalchemy import (Column,and_,
    select, union_all, inspect,null
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func

# 类型变量
T = TypeVar('T', bound='BaseModel')

Base = declarative_base()


class BaseModel(Base):
    """所有模型基类(不自动创建表)"""
    __abstract__ = True
    _source_model = None  # 存储源表模型类
    _session_factory = None  # [新增] 存储会话工厂

    @classmethod
    def set_session_factory(cls, session_factory):
        """设置会话工厂"""
        cls._session_factory = session_factory

    @classmethod
    def get_session(cls):
        """获取数据库会话"""
        if cls._session_factory is None:
            raise ValueError("Session factory not set. Please call set_session_factory() first.")
        return cls._session_factory()

    @classmethod
    def set_source_model(cls, source_model):
        """设置源表模型类"""
        cls._source_model = source_model

    @classmethod
    def get_source_model(cls) -> Optional[Type['BaseModel']]:
        """获取关联的源表模型类"""
        return cls._source_model

    @classmethod
    def get_primary_key(cls) -> Column:
        """获取模型的主键列"""
        pk_columns = inspect(cls).primary_key
        if len(pk_columns) != 1:
            raise ValueError(f"模型 {cls.__name__} 必须要有且只有一个主键")
        return pk_columns[0]

    @classmethod
    def where(cls, *conditions):
        """查询条件"""
        return QuerySet(cls, conditions)

    @classmethod
    def create(cls, **kwargs):
        """创建新记录"""
        if 'is_delete' not in kwargs:
            kwargs['is_delete'] = False

        obj = cls(**kwargs)
        db = cls.get_session()
        try:
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        finally:
            db.close()


class QuerySet(Generic[T]):
    """查询集合，支持从回写表自动合并源表数据"""

    def __init__(self, model_class: Type[T], conditions=None):
        self.model_class = model_class
        self._conditions = conditions or []
        self._limit = None
        self._offset = None
        self._order_by = []
        self._disable_union = False

    def where(self, *conditions):
        """添加查询条件"""
        new_qs = QuerySet(self.model_class, self._conditions + list(conditions))
        new_qs._limit = self._limit
        new_qs._offset = self._offset
        new_qs._order_by = self._order_by.copy()
        new_qs._disable_union = self._disable_union
        return new_qs

    def limit(self, count: int):
        """限制结果数量"""
        self._limit = count
        return self

    def offset(self, offset: int):
        """设置结果偏移量"""
        self._offset = offset
        return self

    def order_by(self, *columns: Union[str, Column]):
        """设置排序字段"""
        self._order_by.extend(columns)
        return self

    def no_union(self):
        """禁用自动合并查询"""
        self._disable_union = True
        return self

    def _build_base_query(self, db):
        """构建基础查询"""
        query = db.query(self.model_class)
        if self._conditions:
            query = query.filter(and_(*self._conditions))
        if self._order_by:
            order_clauses = []
            for order in self._order_by:
                if isinstance(order, str):
                    order = getattr(self.model_class, order)
                order_clauses.append(order)
            query = query.order_by(*order_clauses)
        if self._limit is not None:
            query = query.limit(self._limit)
        if self._offset is not None:
            query = query.offset(self._offset)
        return query

    def _get_source_model(self) -> Optional[Type[T]]:
        """获取关联的源表模型"""
        if self._disable_union:
            return None
        return self.model_class.get_source_model()


    def _map_main_to_writeback(self, source_model):
        """精确的字段映射，确保顺序和类型一致"""
        # 获取回写表的所有列，按原始顺序
        writeback_columns = [c for c in self.model_class.__table__.columns]

        mapping = []
        for wb_col in writeback_columns:
            # 检查主表是否有相同字段
            if hasattr(source_model, wb_col.name):
                main_col = getattr(source_model, wb_col.name)
                mapping.append(main_col.label(wb_col.name))
            else:
                # 只有回写表特有的字段才填充NULL
                mapping.append(null().label(wb_col.name))

        return mapping


    def _build_union_query(self, db):
        source_model = self._get_source_model()
        if not source_model:
            return self._build_base_query(db)

        # 获取主键
        main_pk = source_model.get_primary_key()
        writeback_pk = self.model_class.get_primary_key()
        # 构建字段映射（回写表 → 源表）
        main_select = self._map_main_to_writeback(source_model)
        # 回写表查询（未删除记录）
        writeback_query = select(*self.model_class.__table__.columns).where(
            self.model_class.is_delete == False
        )

        # 源表查询（不在回写表中的记录）
        ontology_query = select(*main_select).where(
            ~main_pk.in_(select(writeback_pk).where(self.model_class.is_delete == False))
        )

        # 先合并两个查询
        union_query = union_all(writeback_query, ontology_query)

        # 将合并查询作为子查询
        subquery = union_query.subquery()

        # 构建最终查询 - 从合并结果中筛选
        final_query = select(*subquery.c)

        # 应用过滤条件到合并后的结果
        if self._conditions:
            # 转换条件中的列引用到子查询的列
            adapted_conditions = []
            for cond in self._conditions:
                if hasattr(cond, 'left') and hasattr(cond.left, 'name'):
                    # 将条件中的列引用转换为子查询的列
                    new_left = subquery.c[cond.left.name]
                    new_cond = cond.__class__(new_left, cond.right, cond.operator)
                    adapted_conditions.append(new_cond)
                else:
                    adapted_conditions.append(cond)

            final_query = final_query.where(and_(*adapted_conditions))

        # 处理排序
        if self._order_by:
            order_clauses = []
            for order in self._order_by:
                if isinstance(order, str):
                    if hasattr(subquery.c, order):
                        order_clauses.append(subquery.c[order])
                    else:
                        raise AttributeError(f"排序字段 '{order}' 不存在")
                else:
                    order_clauses.append(order)
            final_query = final_query.order_by(*order_clauses)

        # 添加分页
        if self._limit is not None:
            final_query = final_query.limit(self._limit)
        if self._offset is not None:
            final_query = final_query.offset(self._offset)
        return final_query

    def all(self) -> List[T]:
        """获取所有结果"""
        db = self.model_class.get_session()
        try:
            if self._get_source_model():
                result = db.execute(self._build_union_query(db))
                return [self.model_class(**dict(row._mapping)) for row in result]
            return self._build_base_query(db).all()
        finally:
            db.close()

    def first(self) -> Optional[T]:
        """获取第一个结果"""
        db = self.model_class.get_session()
        try:
            if self._get_source_model():
                result = db.execute(self._build_union_query(db)).first()
                return self.model_class(**dict(result)) if result else None
            return self._build_base_query(db).first()
        finally:
            db.close()

    def count(self) -> int:
        """计数"""
        db = self.model_class.get_session()
        try:
            if self._get_source_model():
                union_query = self._build_union_query(db)
                count_query = select(func.count()).select_from(union_query.alias())
                return db.execute(count_query).scalar()
            return self._build_base_query(db).count()
        finally:
            db.close()

    def update(self, **kwargs) -> int:
        """批量更新"""
        source_model = self._get_source_model()
        if not source_model:
            # 没有源表，直接更新
            db = self.model_class.get_session()
            try:
                query = db.query(self.model_class)
                if self._conditions:
                    query = query.filter(and_(*self._conditions))
                result = query.update(kwargs)
                db.commit()
                return result
            except SQLAlchemyError as e:
                db.rollback()
                raise e
            finally:
                db.close()

        # 处理有源表的情况
        db = self.model_class.get_session()
        try:
            # 1. 先查询符合条件的记录
            query = self._build_union_query(db)
            records = db.execute(query).fetchall()
            # 2. 对每条记录处理
            affected = 0
            pk_name = self.model_class.get_primary_key().name

            for record in records:
                # 获取主键值
                pk_value = getattr(record, pk_name)

                # 检查回写表是否已有记录
                existing = db.query(self.model_class).filter(
                    getattr(self.model_class, pk_name) == pk_value
                ).first()


                if existing:
                    # 更新现有记录
                    print(kwargs)
                    print(existing.new_filed)
                    for key, value in kwargs.items():
                        if hasattr(existing, key):
                            setattr(existing, key, value)

                    affected += 1
                else:
                    # 创建新记录
                    new_data = {**dict(record), **kwargs}
                    new_data['is_delete'] = False
                    new_record = self.model_class(**new_data)
                    db.add(new_record)
                    affected += 1

            db.commit()
            return affected
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def delete(self) -> int:
        """批量删除"""
        source_model = self._get_source_model()
        if not source_model:
            # 没有源表，物理删除
            db = self.model_class.get_session()
            try:
                query = db.query(self.model_class)
                if self._conditions:
                    query = query.filter(and_(*self._conditions))
                result = query.delete()
                db.commit()
                return result
            except SQLAlchemyError as e:
                db.rollback()
                raise e
            finally:
                db.close()

        # 处理有源表的情况
        db = self.model_class.get_session()
        try:
            # 1. 先查询符合条件的记录
            query = self._build_union_query(db)
            records = db.execute(query).fetchall()

            # 2. 对每条记录处理
            affected = 0
            pk_name = self.model_class.get_primary_key().name

            for record in records:
                # 获取主键值
                pk_value = getattr(record, pk_name)

                # 检查回写表是否已有记录
                existing = db.query(self.model_class).filter(
                    getattr(self.model_class, pk_name) == pk_value
                ).first()

                if existing:
                    # 标记删除
                    existing.is_delete = True
                    affected += 1
                else:
                    # 创建删除记录
                    delete_data = {
                        pk_name: pk_value,
                    }
                    # 设置其他必要字段
                    for column in self.model_class.__table__.columns:
                        if column.name != pk_name and hasattr(record, column.name):
                            delete_data[column.name] = getattr(record, column.name)
                    delete_data['is_delete'] = True
                    delete_record = self.model_class(**delete_data)
                    db.add(delete_record)
                    affected += 1

            db.commit()
            return affected
        except SQLAlchemyError as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def __iter__(self):
        return iter(self.all())


class FoundryClient:
    """操作客户端"""

    def __init__(self, session_factory):
        self._session_factory = session_factory
        self.ontology = OntologyNamespace(self._session_factory)



class OntologyNamespace:
    def __init__(self,session_factory):
        self.objects = ObjectNamespace(session_factory)


class ObjectNamespace:
    """动态模型查询集命名空间"""

    def __init__(self,session_factory):
        self._session_factory = session_factory
        self._model_classes = {
            cls.__name__: cls
            for cls in BaseModel.__subclasses__()
        }
        for model_class in self._model_classes.values():
            model_class.set_session_factory(session_factory)

    def __getattr__(self, name):
        if name in self._model_classes:
            model_class = self._model_classes[name]

            class HybridQuerySet(QuerySet):
                @classmethod
                def create(cls, **kwargs):
                    return model_class.create(**kwargs)

            return HybridQuerySet(model_class)
        raise AttributeError(f"Model '{name}' not found")

