"""Initial revision

Revision ID: 53ad5b825e2c
Revises: 25bc5992cb40
Create Date: 2024-10-21 19:26:15.602250

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53ad5b825e2c'
down_revision: Union[str, None] = '25bc5992cb40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('author_picture', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('genre', sa.String(), nullable=True),
    sa.Column('publisher', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('book_picture', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['authors.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('orders', sa.Column('books_id', sa.Integer(), nullable=True))
    op.alter_column('orders', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'orders', 'books', ['books_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.alter_column('orders', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('orders', 'books_id')
    op.drop_table('books')
    op.drop_table('authors')
    # ### end Alembic commands ###
