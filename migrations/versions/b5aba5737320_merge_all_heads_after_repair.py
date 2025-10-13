"""merge all heads after repair

Revision ID: b5aba5737320
Revises: add_muscle_measurements, create_contact_msgs, merge_heads_profile_picture
Create Date: 2025-10-07 22:46:56.601991

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b5aba5737320"
down_revision = (
    "add_muscle_measurements",
    "create_contact_msgs",
    "merge_heads_profile_picture",
)
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
