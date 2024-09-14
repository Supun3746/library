"""usernamame unique True

Revision ID: b48ad55816bd
Revises: ca742180b791
Create Date: 2024-09-14 13:09:10.396139

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b48ad55816bd"
down_revision: Union[str, None] = "ca742180b791"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_unique_constraint("uq_users_username", ["username"])


def downgrade() -> None:
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("uq_users_username", type_="unique")
