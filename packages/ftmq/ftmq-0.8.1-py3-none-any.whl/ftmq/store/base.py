from typing import Iterable

from nomenklatura import store as nk
from nomenklatura.resolver import Resolver

from ftmq.aggregations import AggregatorResult
from ftmq.logging import get_logger
from ftmq.model.coverage import Collector, DatasetStats
from ftmq.model.dataset import C, Dataset
from ftmq.query import Q
from ftmq.types import CE, CEGenerator
from ftmq.util import DefaultDataset, ensure_dataset, make_dataset

log = get_logger(__name__)


class Store(nk.Store):
    """
    Feature add-ons to `nomenklatura.store.Store`
    """

    def __init__(
        self,
        catalog: C | None = None,
        dataset: Dataset | str | None = None,
        linker: Resolver | None = None,
        **kwargs,
    ) -> None:
        """
        Initialize a store. This should be called via
        [`get_store`][ftmq.store.get_store]

        Args:
            catalog: A `ftmq.model.Catalog` instance to limit the scope to
            dataset: A `ftmq.model.Dataset` instance to limit the scope to
            linker: A `nomenklatura.Resolver` instance with linked / deduped data
        """
        if dataset is not None:
            if isinstance(dataset, str):
                dataset = Dataset(name=dataset)
            dataset = make_dataset(dataset.name)
        elif catalog is not None:
            dataset = catalog.get_scope()
        else:
            dataset = DefaultDataset
        super().__init__(dataset=dataset, linker=linker or Resolver(), **kwargs)
        # implicit set all datasets as default store scope:
        if dataset == DefaultDataset:
            self.dataset = self.get_catalog().get_scope()

    def get_catalog(self) -> C:
        """
        Return implicit `Catalog` computed from current datasets in store
        """
        raise NotImplementedError

    def iterate(self, dataset: str | Dataset | None = None) -> CEGenerator:
        """
        Iterate all the entities, optional filter for a dataset.

        Args:
            dataset: `Dataset` instance or name to limit scope to

        Yields:
            Generator of `nomenklatura.entity.CompositeEntity`
        """
        dataset = ensure_dataset(dataset)
        if dataset is not None:
            view = self.view(dataset)
        else:
            catalog = self.get_catalog()
            view = self.view(catalog.get_scope())
        yield from view.entities()

    def resolve(self, dataset: str | Dataset | None = None) -> None:
        if not self.linker.edges:
            return
        if dataset is not None:
            if isinstance(dataset, str):
                dataset = make_dataset(dataset)
            elif isinstance(dataset, Dataset):
                dataset = make_dataset(dataset.name)
            view = self.view(scope=dataset)
            entities = view.entities()
        else:
            entities = self.iterate()
        for ix, entity in enumerate(entities):
            if entity.id in self.linker.nodes:
                self.update(self.linker.get_canonical(entity.id))
            if ix and ix % 10_000 == 0:
                log.info("Resolving entity %d ..." % ix)


class View(nk.base.View):
    """
    Feature add-ons to `nomenklatura.store.base.View`
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}

    def entities(self, query: Q | None = None) -> CEGenerator:
        """
        Get the entities of a store, optionally filtered by a
        [`Query`][ftmq.Query] object.

        Args:
            query: The Query filter object

        Yields:
            Generator of `nomenklatura.entity.CompositeEntity`
        """
        view = self.store.view(self.scope)
        if query:
            yield from query.apply_iter(view.entities())
        else:
            yield from view.entities()

    def get_adjacents(
        self, proxies: Iterable[CE], inverted: bool | None = False
    ) -> set[CE]:
        seen: set[CE] = set()
        for proxy in proxies:
            for _, adjacent in self.get_adjacent(proxy, inverted=inverted):
                if adjacent.id not in seen:
                    seen.add(adjacent)
        return seen

    def stats(self, query: Q | None = None) -> DatasetStats:
        key = f"stats-{hash(query)}"
        if key in self._cache:
            return self._cache[key]
        c = Collector()
        cov = c.collect_many(self.entities(query))
        self._cache[key] = cov
        return cov

    def aggregations(self, query: Q) -> AggregatorResult | None:
        if not query.aggregations:
            return
        key = f"agg-{hash(query)}"
        if key in self._cache:
            return self._cache[key]
        _ = [x for x in self.entities(query)]
        res = dict(query.aggregator.result)
        self._cache[key] = res
        return res
