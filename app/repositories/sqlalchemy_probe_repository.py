from typing import Optional, List

from .probe_repository import IProbeRepository
from .database_models import ProbeDB
from app.domain.models import Probe, Grid, Position
from app.domain.state import Direction


class SQLAlchemyProbeRepository(IProbeRepository):
    """
    Implementação do repositório que usa o SQLAlchemy para persistir
    os dados das sondas em um banco de dados.
    """

    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    def _to_domain(self, probe_db: ProbeDB) -> Probe:
        """Converte o modelo do banco de dados (ORM) para o modelo de domínio."""
        grid = Grid(max_x=probe_db.max_x, max_y=probe_db.max_y)
        position = Position(x=probe_db.x, y=probe_db.y)
        direction_enum = Direction(probe_db.direction)

        probe = Probe(
            grid=grid,
            initial_direction=direction_enum,
            probe_id=probe_db.id,
            initial_position=position
        )
        return probe

    def save(self, probe: Probe) -> None:
        with self.db_session_factory() as db:
            probe_db = db.get(ProbeDB, probe.id)
            if probe_db:
                probe_db.x = probe.position.x
                probe_db.y = probe.position.y
                probe_db.direction = probe.current_direction.value
                probe_db.max_x = probe.grid.max_x
                probe_db.max_y = probe.grid.max_y
            else:
                probe_db = ProbeDB(
                    id=probe.id,
                    x=probe.position.x,
                    y=probe.position.y,
                    direction=probe.current_direction.value,
                    max_x=probe.grid.max_x,
                    max_y=probe.grid.max_y,
                )
                db.add(probe_db)
            db.commit()

    def get_by_id(self, probe_id: str) -> Optional[Probe]:
        with self.db_session_factory() as db:
            probe_db = db.get(ProbeDB, probe_id)
            if probe_db:
                return self._to_domain(probe_db)
            return None

    def get_all(self) -> List[Probe]:
        with self.db_session_factory() as db:
            all_probes_db = db.query(ProbeDB).all()
            return [self._to_domain(p) for p in all_probes_db]