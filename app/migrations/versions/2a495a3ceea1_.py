"""empty message

Revision ID: 2a495a3ceea1
Revises: 
Create Date: 2022-08-14 20:57:12.474460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a495a3ceea1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('Clientid', sa.Integer(), nullable=False),
    sa.Column('CliName', sa.String(length=50), nullable=False),
    sa.Column('CliEmail', sa.String(length=50), nullable=False),
    sa.Column('CliTel', sa.String(length=20), nullable=False),
    sa.Column('CliPass', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('Clientid'),
    sa.UniqueConstraint('CliEmail'),
    sa.UniqueConstraint('CliTel')
    )
    op.create_table('drone_bases',
    sa.Column('DronBaseid', sa.Integer(), nullable=False),
    sa.Column('CompanyName', sa.String(length=30), nullable=False),
    sa.Column('CompanyPass', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('DronBaseid'),
    sa.UniqueConstraint('CompanyName'),
    sa.UniqueConstraint('CompanyPass')
    )
    op.create_table('roles',
    sa.Column('Roleid', sa.Integer(), nullable=False),
    sa.Column('RoleName', sa.String(length=50), nullable=False),
    sa.Column('RoleDesc', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('Roleid')
    )
    op.create_table('drons',
    sa.Column('Dronid', sa.Integer(), nullable=False),
    sa.Column('DronModle', sa.String(length=15), nullable=False),
    sa.Column('EnergyCapacity', sa.Integer(), nullable=False),
    sa.Column('LiftingCapacity', sa.Integer(), nullable=False),
    sa.Column('DrDronBaseid', sa.Integer(), nullable=False),
    sa.Column('IsOccupied', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['DrDronBaseid'], ['drone_bases.DronBaseid'], ),
    sa.PrimaryKeyConstraint('Dronid')
    )
    op.create_table('tasks',
    sa.Column('Taskid', sa.Integer(), nullable=False),
    sa.Column('Dist', sa.Integer(), nullable=False),
    sa.Column('Weight', sa.Integer(), nullable=False),
    sa.Column('TaskDesc', sa.String(length=200), nullable=False),
    sa.Column('Date', sa.DateTime(), nullable=False),
    sa.Column('IsOccupied', sa.Boolean(), nullable=True),
    sa.Column('Task_Clientid', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Task_Clientid'], ['clients.Clientid'], ),
    sa.PrimaryKeyConstraint('Taskid')
    )
    op.create_table('users',
    sa.Column('Userid', sa.Integer(), nullable=False),
    sa.Column('UserName', sa.String(length=50), nullable=False),
    sa.Column('UserEmail', sa.String(length=50), nullable=False),
    sa.Column('UserTel', sa.String(length=20), nullable=True),
    sa.Column('UserPass', sa.String(length=500), nullable=False),
    sa.Column('UserRoleid', sa.Integer(), nullable=False),
    sa.Column('UserDronBaseid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['UserDronBaseid'], ['drone_bases.DronBaseid'], ),
    sa.ForeignKeyConstraint(['UserRoleid'], ['roles.Roleid'], ),
    sa.PrimaryKeyConstraint('Userid'),
    sa.UniqueConstraint('UserEmail'),
    sa.UniqueConstraint('UserTel')
    )
    op.create_table('dron_on_task_statistic',
    sa.Column('Statisticid', sa.Integer(), nullable=False),
    sa.Column('Status', sa.Boolean(), nullable=False),
    sa.Column('Dronid', sa.Integer(), nullable=False),
    sa.Column('TaskDesc', sa.String(), nullable=False),
    sa.Column('DronBaseid', sa.Integer(), nullable=False),
    sa.Column('Data', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['DronBaseid'], ['drone_bases.DronBaseid'], ),
    sa.ForeignKeyConstraint(['Dronid'], ['drons.Dronid'], ),
    sa.PrimaryKeyConstraint('Statisticid')
    )
    op.create_table('drons_on_tasks',
    sa.Column('DronTaskid', sa.Integer(), nullable=False),
    sa.Column('Date', sa.DateTime(), nullable=False),
    sa.Column('DoTDronid', sa.Integer(), nullable=True),
    sa.Column('DoTTaskid', sa.Integer(), nullable=True),
    sa.Column('DoTBaseid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['DoTBaseid'], ['drone_bases.DronBaseid'], ),
    sa.ForeignKeyConstraint(['DoTDronid'], ['drons.Dronid'], ),
    sa.ForeignKeyConstraint(['DoTTaskid'], ['tasks.Taskid'], ),
    sa.PrimaryKeyConstraint('DronTaskid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('drons_on_tasks')
    op.drop_table('dron_on_task_statistic')
    op.drop_table('users')
    op.drop_table('tasks')
    op.drop_table('drons')
    op.drop_table('roles')
    op.drop_table('drone_bases')
    op.drop_table('clients')
    # ### end Alembic commands ###
