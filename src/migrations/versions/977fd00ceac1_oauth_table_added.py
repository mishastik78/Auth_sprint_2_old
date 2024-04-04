"""oauth table added

Revision ID: 977fd00ceac1
Revises: 5c5f28844804
Create Date: 2022-08-10 13:23:56.785505

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '977fd00ceac1'
down_revision = '5c5f28844804'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('o_auth_account',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('issuer', sa.String(length=255), nullable=False),
    sa.Column('sub', sa.String(length=1024), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'issuer')
    )
    op.create_unique_constraint(None, 'role', ['id'])
    op.create_unique_constraint(None, 'user', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'role', type_='unique')
    op.drop_table('o_auth_account')
    # ### end Alembic commands ###
