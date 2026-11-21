"""Create users, posts and votes tables."""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("email", sa.String(length=255), nullable=False), sa.Column("password", sa.String(length=255), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table("posts", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(length=200), nullable=False), sa.Column("content", sa.Text(), nullable=False), sa.Column("published", sa.Boolean(), server_default=sa.text("1"), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False))
    op.create_index("ix_posts_title", "posts", ["title"])
    op.create_index("ix_posts_owner_id", "posts", ["owner_id"])
    op.create_table("votes", sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True), sa.Column("post_id", sa.Integer(), sa.ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True))


def downgrade():
    op.drop_table("votes")
    op.drop_index("ix_posts_owner_id", table_name="posts")
    op.drop_index("ix_posts_title", table_name="posts")
    op.drop_table("posts")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
