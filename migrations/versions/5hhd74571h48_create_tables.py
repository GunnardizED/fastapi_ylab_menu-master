"""create tables

Revision ID: 5hhd74571h48
Revises:
Create Date: 2023-08-13 22:07:18.289657

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "5hhd74571h48"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "menu",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "description",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_menu_id"), "menu", ["id"], unique=True)
    op.create_table(
        "submenu",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "description",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column("menu_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(["menu_id"], ["menu.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_submenu_id"), "submenu", ["id"], unique=True)
    op.create_index(
        op.f("ix_submenu_menu_id"),
        "submenu",
        ["menu_id"],
        unique=False,
    )
    op.create_table(
        "dish",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "description",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column("price", sa.Numeric(scale=2), nullable=True),
        sa.Column("submenu_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.ForeignKeyConstraint(["submenu_id"], ["submenu.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dish_id"), "dish", ["id"], unique=True)
    op.create_index(
        op.f("ix_dish_submenu_id"),
        "dish",
        ["submenu_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_dish_submenu_id"), table_name="dish")
    op.drop_index(op.f("ix_dish_id"), table_name="dish")
    op.drop_table("dish")
    op.drop_index(op.f("ix_submenu_menu_id"), table_name="submenu")
    op.drop_index(op.f("ix_submenu_id"), table_name="submenu")
    op.drop_table("submenu")
    op.drop_index(op.f("ix_menu_id"), table_name="menu")
    op.drop_table("menu")
    # ### end Alembic commands ###
