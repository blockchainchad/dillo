"""Subscription setting for notification

Revision ID: 42809264a67e
Revises: 477678dfd050
Create Date: 2015-07-08 02:10:47.761444

"""

# revision identifiers, used by Alembic.
revision = '42809264a67e'
down_revision = '477678dfd050'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification_subscriptions', sa.Column('is_subscribed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notification_subscriptions', 'is_subscribed')
    ### end Alembic commands ###