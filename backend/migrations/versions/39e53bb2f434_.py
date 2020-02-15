"""created user

Revision ID: 39e53bb2f434
Revises: 
Create Date: 2020-02-12 20:13:00.568017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39e53bb2f434'
down_revision = None
branch_labels = None
depends_on = None

privacy_type = sa.Enum('ALL', 'AUTHORIZED', 'HIDDEN', name='privacytype')


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=70), nullable=False),
    sa.Column('identity', sa.String(length=36), nullable=False),
    sa.Column('privacy', privacy_type, nullable=False),
    sa.Column('is_active', sa.Boolean(create_constraint=False), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
    privacy_type.drop(op.get_bind(), checkfirst=True)
