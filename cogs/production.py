import sqlite3
import asyncio
import discord
from discord.ext import commands
from discord.utils import get

new_line = '\n'
# Connect to the sqlite DB (it will create a new DB if it doesn't exit)
conn = sqlite3.connect('player_info.db')
cursor = conn.cursor()


class Production(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def res(self, ctx):
        user_id = ctx.author.id

        # fetch user nation_name
        cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            user_id, nation_name, turns_accumulated, gov_type, tax_rate, conscription, freedom, police_policy, fire_policy, hospital_policy, war_status, happiness = result

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (nation_name,))
            res_result = cursor.fetchone()

            # fetch user's production infra
            cursor.execute(
                'SELECT name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory FROM infra WHERE name = ?',
                (nation_name,))
            infra_result = cursor.fetchone()

            # fetch user's military stats
            cursor.execute(
                'SELECT name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory FROM user_mil WHERE name_nation = ?',
                (nation_name,))
            mil_result = cursor.fetchone()

            # fetch user's population stats.
            cursor.execute(
                'SELECT name, nation_score, gdp, adult, balance FROM user_stats WHERE name = ?',
                (nation_name,))
            pop_result = cursor.fetchone()


            if infra_result and res_result:
                name, basic_house, small_flat, apt_complex, skyscraper, lumber_mill, coal_mine, iron_mine, lead_mine, bauxite_mine, oil_derrick, uranium_mine, farm, aluminium_factory, steel_factory, oil_refinery, ammo_factory, concrete_factory, militaryfactory = infra_result
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = res_result
                name_nation, troops, planes, weapon, tanks, artillery, anti_air, barracks, tank_factory, plane_factory, artillery_factory, anti_air_factory = mil_result
                name, nation_score, gdp, adult, balance = pop_result

                # the production of military equipment.
                prod_aa = anti_air_factory * militaryfactory // 40
                prod_arty = artillery_factory * militaryfactory // 40
                prod_plane = plane_factory * militaryfactory // 45
                prod_tank = tank_factory * militaryfactory // 42 

                # The production of each resource
                prod_wood = lumber_mill * 2
                prod_coal = coal_mine * 1.2
                prod_iron = iron_mine * 1
                prod_lead = lead_mine * 0.8
                prod_bauxite = bauxite_mine * 0.6
                prod_oil = oil_derrick * 1
                prod_uranium = uranium_mine * 0.05
                prod_farm = farm * 10
                prod_aluminium = aluminium_factory * 0.4
                prod_steel = steel_factory * 0.3
                prod_gas = oil_refinery * 0.2
                prod_ammo = ammo_factory * 0.5
                prod_concrete = concrete_factory * 0.6


                # The consumption of each resource
                usage_iron_wood = prod_wood * 0
                usage_lead_wood = prod_wood * 0
                usage_bauxite_wood = prod_wood * 0
                usage_iron_coal = prod_coal * 0
                usage_lead_coal = prod_coal * 0
                usage_bauxite_coal = prod_coal * 0
                usage_iron_iron = prod_iron * 0
                usage_lead_iron = prod_iron * 0
                usage_bauxite_iron = prod_iron * 0
                usage_iron_lead = prod_lead * 0
                usage_lead_lead = prod_lead * 0
                usage_bauxite_lead = prod_lead * 0
                usage_iron_bauxite = prod_bauxite * 0
                usage_lead_bauxite = prod_bauxite * 0
                usage_bauxite_bauxite = prod_bauxite * 0
                usage_iron_oil = prod_oil * 0
                usage_lead_oil = prod_oil * 0
                usage_bauxite_oil = prod_oil * 0
                usage_iron_uranium = prod_uranium * 0
                usage_lead_uranium = prod_uranium * 0
                usage_bauxite_uranium = prod_uranium * 0
                usage_iron_food = prod_farm * 0
                usage_lead_food = prod_farm * 0
                usage_bauxite_food = prod_farm * 0
                usage_iron_aluminium = prod_aluminium * 0.2
                usage_lead_aluminium = prod_aluminium * 0.1
                usage_bauxite_aluminium = prod_aluminium * 1.2
                usage_iron_steel = prod_steel * 1.4
                usage_lead_steel = prod_steel * 0.3
                usage_bauxite_steel = prod_steel * 0.3
                usage_oil_gas = prod_gas * 2
                usage_lead_gas = prod_gas * 0
                usage_bauxite_gas = prod_gas * 0
                usage_iron_ammo = prod_ammo * 0.2
                usage_lead_ammo = prod_ammo * 1.1
                usage_bauxite_ammo = prod_ammo * 0
                usage_iron_concrete = prod_concrete * 0.5
                usage_lead_concrete = prod_concrete * 0
                usage_bauxite_concrete = prod_concrete * 0

                final_usage_iron = usage_iron_wood + usage_iron_coal + usage_iron_iron + usage_iron_lead + usage_iron_bauxite + usage_iron_oil + usage_iron_uranium + usage_iron_food + usage_iron_aluminium + usage_iron_steel + usage_iron_ammo + usage_iron_concrete
                final_usage_lead = usage_lead_wood + usage_lead_coal + usage_lead_iron + usage_lead_lead + usage_lead_bauxite + usage_lead_oil + usage_lead_uranium + usage_lead_food + usage_lead_aluminium + usage_lead_steel + usage_lead_ammo + usage_lead_concrete
                final_usage_bauxite = usage_bauxite_wood + usage_bauxite_coal + usage_bauxite_iron + usage_bauxite_lead + usage_bauxite_bauxite + usage_bauxite_oil + usage_bauxite_uranium + usage_bauxite_food + usage_bauxite_aluminium + usage_bauxite_steel + usage_bauxite_ammo + usage_bauxite_concrete

                final_prod_iron = prod_iron - final_usage_iron
                final_prod_lead = prod_lead - final_usage_lead
                final_prod_bauxite = prod_bauxite - final_usage_bauxite
                final_prod_oil = prod_oil - usage_oil_gas

                total_pop = adult
                usage_food = total_pop // 50

                final_prod_food = prod_farm - usage_food

                if (iron < final_usage_iron) or (lead < final_usage_lead) or (bauxite < final_usage_bauxite) or (oil < usage_oil_gas):
                    prod_aluminium = 0
                    prod_steel = 0
                    prod_gas = 0
                    prod_ammo = 0
                    prod_concrete = 0


                    main_emb = discord.Embed(title='Production', type='rich',
                                            description=f'Displays {name}\'s production.\n'
                                                        'React with "⛏" for Mined Resources.\n'
                                                        'React with "🏭" for Manufactured Resources.\n'
                                                        'React with "🛡" for Military Equipment.',
                                            color=discord.Color.blue()
                                            )

                    mined_emb = discord.Embed(title="Mined Resources", type='rich',
                                            description=f'Displays {name}\'s Mined Resources Production.',
                                            color=discord.Color.blue()
                                            )
                    mined_emb.add_field(name='Wood', value=f'{prod_wood:,}', inline=False)
                    mined_emb.add_field(name='Coal', value=f'{prod_coal:,}', inline=False)
                    mined_emb.add_field(name='Iron', value=f'{final_prod_iron:,}', inline=False)
                    mined_emb.add_field(name='Lead', value=f'{final_prod_lead:,}', inline=False)
                    mined_emb.add_field(name='Bauxite', value=f'{final_prod_bauxite:,}', inline=False)
                    mined_emb.add_field(name='Oil', value=f'{final_prod_oil:,}', inline=False)
                    mined_emb.add_field(name='Uranium', value=f'{prod_uranium:,}', inline=False)
                    mined_emb.add_field(name='Food', value=f'{final_prod_food:,}', inline=False)

                    manu_emb = discord.Embed(title='Manufactured Resources', type='rich',
                                            description=f'Displays {name}\'s Mined Resources Production.',
                                            color=discord.Color.blue()
                                            )
                    manu_emb.add_field(name='Aluminium', value=f'{prod_aluminium:,}', inline=False)
                    manu_emb.add_field(name='Steel', value=f'{prod_steel:,}', inline=False)
                    manu_emb.add_field(name='Gasoline', value=f'{prod_gas:,}', inline=False)
                    manu_emb.add_field(name='Ammo', value=f'{prod_ammo:,}', inline=False)
                    manu_emb.add_field(name='Concrete', value=f'{prod_concrete:,}', inline=False)

                    mil_emb = discord.Embed(title='Military Equipment', type='rich',
                                            description=f'Displays {name}\'s Military Equipment Production.',
                                            color=discord.Color.blue()
                                            )
                    mil_emb.add_field(name='Tanks', value=f'{prod_tank:,}', inline=False)
                    mil_emb.add_field(name='Plane', value=f'{prod_plane:,}', inline=False)
                    mil_emb.add_field(name='Artillery', value=f'{prod_arty:,}', inline=False)
                    mil_emb.add_field(name='Anti-Air', value=f'{prod_aa:,}', inline=False)

                    prod_emb = await ctx.send(embed=main_emb)
                    await prod_emb.add_reaction("⛏")
                    await prod_emb.add_reaction("🏭")
                    await prod_emb.add_reaction("🛡")

                    def chk(rec, usr):
                        return usr == ctx.author and str(rec.emoji) in ['⛏', '🏭', '🛡']

                    while True:
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=chk)
                        except TimeoutError:
                            break
                        match(str(reaction.emoji)):   # Choosing Tab based on emoji
                            case '⛏':
                                await prod_emb.edit(embed=mined_emb)
                            case '🏭':
                                await prod_emb.edit(embed=manu_emb)
                            case '🛡':
                                await prod_emb.edit(embed=mil_emb)
                            case _:
                                break
                        await prod_emb.remove_reaction(reaction.emoji, user)

                if gov_type == "Communism":
                    # The production of each resource
                    com_prod_wood = lumber_mill * 2 * 2
                    com_prod_coal = coal_mine * 1.2 * 2
                    com_prod_iron = iron_mine * 1 * 2
                    com_prod_lead = lead_mine * 0.8 * 2
                    com_prod_bauxite = bauxite_mine * 0.6 * 2
                    com_prod_oil = oil_derrick * 1 * 2
                    com_prod_uranium = uranium_mine * 0.05 * 2
                    com_prod_farm = farm * 10 * 2
                    com_prod_aluminium = aluminium_factory * 0.4 * 2
                    com_prod_steel = steel_factory * 0.3 * 2
                    com_prod_gas = oil_refinery * 0.2 * 2
                    com_prod_ammo = ammo_factory * 0.5 * 2
                    com_prod_concrete = concrete_factory * 0.6 * 2

                    final_prod_iron = com_prod_iron - final_usage_iron
                    final_prod_lead = com_prod_lead - final_usage_lead
                    final_prod_bauxite = com_prod_bauxite - final_usage_bauxite
                    final_prod_oil = com_prod_oil - usage_oil_gas
                    final_prod_food = com_prod_farm - usage_food


                    main_emb = discord.Embed(title='Production', type='rich',
                                            description=f'Displays {name}\'s production.\n'
                                                        'React with "⛏" for Mined Resources.\n'
                                                        'React with "🏭" for Manufactured Resources.\n'
                                                        'React with "🛡" for Military Equipment.',
                                            color=discord.Color.blue()
                                            )

                    mined_emb = discord.Embed(title="Mined Resources", type='rich',
                                            description=f'Displays {name}\'s Mined Resources Production.',
                                            color=discord.Color.blue()
                                            )
                    mined_emb.add_field(name='Wood', value=f'{com_prod_wood:,}', inline=False)
                    mined_emb.add_field(name='Coal', value=f'{com_prod_coal:,}', inline=False)
                    mined_emb.add_field(name='Iron', value=f'{final_prod_iron:,}', inline=False)
                    mined_emb.add_field(name='Lead', value=f'{final_prod_lead:,}', inline=False)
                    mined_emb.add_field(name='Bauxite', value=f'{final_prod_bauxite:,}', inline=False)
                    mined_emb.add_field(name='Oil', value=f'{final_prod_oil:,}', inline=False)
                    mined_emb.add_field(name='Uranium', value=f'{com_prod_uranium:,}', inline=False)
                    mined_emb.add_field(name='Food', value=f'{final_prod_food:,}', inline=False)

                    manu_emb = discord.Embed(title='Manufactured Resources', type='rich',
                                            description=f'Displays {name}\'s Mined Resources Production.',
                                            color=discord.Color.blue()
                                            )
                    manu_emb.add_field(name='Aluminium', value=f'{com_prod_aluminium:,}', inline=False)
                    manu_emb.add_field(name='Steel', value=f'{com_prod_steel:,}', inline=False)
                    manu_emb.add_field(name='Gasoline', value=f'{com_prod_gas:,}', inline=False)
                    manu_emb.add_field(name='Ammo', value=f'{com_prod_ammo:,}', inline=False)
                    manu_emb.add_field(name='Concrete', value=f'{com_prod_concrete:,}', inline=False)

                    mil_emb = discord.Embed(title='Military Equipment', type='rich',
                                            description=f'Displays {name}\'s Military Equipment Production.',
                                            color=discord.Color.blue()
                                            )
                    mil_emb.add_field(name='Tanks', value=f'{prod_tank:,}', inline=False)
                    mil_emb.add_field(name='Plane', value=f'{prod_plane:,}', inline=False)
                    mil_emb.add_field(name='Artillery', value=f'{prod_arty:,}', inline=False)
                    mil_emb.add_field(name='Anti-Air', value=f'{prod_aa:,}', inline=False)

                    prod_emb = await ctx.send(embed=main_emb)
                    await prod_emb.add_reaction("⛏")
                    await prod_emb.add_reaction("🏭")
                    await prod_emb.add_reaction("🛡")

                    def chk(rec, usr):
                        return usr == ctx.author and str(rec.emoji) in ['⛏', '🏭', '🛡']

                    while True:
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=chk)
                        except TimeoutError:
                            break
                        match(str(reaction.emoji)):   # Choosing Tab based on emoji
                            case '⛏':
                                await prod_emb.edit(embed=mined_emb)
                            case '🏭':
                                await prod_emb.edit(embed=manu_emb)
                            case '🛡':
                                await prod_emb.edit(embed=mil_emb)
                            case _:
                                break
                        await prod_emb.remove_reaction(reaction.emoji, user)


                main_emb = discord.Embed(title='Production', type='rich',
                                            description=f'Displays {name}\'s production.\n'
                                                        'React with "⛏" for Mined Resources.\n'
                                                        'React with "🏭" for Manufactured Resources.\n'
                                                        'React with "🛡" for Military Equipment.',
                                            color=discord.Color.blurple()
                                            )

                mined_emb = discord.Embed(title="Mined Resources", type='rich',
                                        description=f'Displays {name}\'s Mined Resources Production.',
                                        color=discord.Color.blurple()
                                        )
                mined_emb.add_field(name='Wood', value=f'{prod_wood:,}', inline=False)
                mined_emb.add_field(name='Coal', value=f'{prod_coal:,}', inline=False)
                mined_emb.add_field(name='Iron', value=f'{final_prod_iron:,}', inline=False)
                mined_emb.add_field(name='Lead', value=f'{final_prod_lead:,}', inline=False)
                mined_emb.add_field(name='Bauxite', value=f'{final_prod_bauxite:,}', inline=False)
                mined_emb.add_field(name='Oil', value=f'{final_prod_oil:,}', inline=False)
                mined_emb.add_field(name='Uranium', value=f'{prod_uranium:,}', inline=False)
                mined_emb.add_field(name='Food', value=f'{final_prod_food:,}', inline=False)

                manu_emb = discord.Embed(title='Manufactured Resources', type='rich',
                                        description=f'Displays {name}\'s Mined Resources Production.',
                                        color=discord.Color.blurple()
                                        )
                manu_emb.add_field(name='Aluminium', value=f'{prod_aluminium:,}', inline=False)
                manu_emb.add_field(name='Steel', value=f'{prod_steel:,}', inline=False)
                manu_emb.add_field(name='Gasoline', value=f'{prod_gas:,}', inline=False)
                manu_emb.add_field(name='Ammo', value=f'{prod_ammo:,}', inline=False)
                manu_emb.add_field(name='Concrete', value=f'{prod_concrete:,}', inline=False)

                mil_emb = discord.Embed(title='Military Equipment', type='rich',
                                        description=f'Displays {name}\'s Military Equipment Production.',
                                        color=discord.Color.blurple()
                                        )
                mil_emb.add_field(name='Tanks', value=f'{prod_tank:,}', inline=False)
                mil_emb.add_field(name='Plane', value=f'{prod_plane:,}', inline=False)
                mil_emb.add_field(name='Artillery', value=f'{prod_arty:,}', inline=False)
                mil_emb.add_field(name='Anti-Air', value=f'{prod_aa:,}', inline=False)

                prod_emb = await ctx.send(embed=main_emb)
                await prod_emb.add_reaction("⛏")
                await prod_emb.add_reaction("🏭")
                await prod_emb.add_reaction("🛡")

                def chk(rec, usr):
                    return usr == ctx.author and str(rec.emoji) in ['⛏', '🏭', '🛡']

                while True:
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=60, check=chk)
                    except TimeoutError:
                        break
                    match(str(reaction.emoji)):   # Choosing Tab based on emoji
                        case '⛏':
                            await prod_emb.edit(embed=mined_emb)
                        case '🏭':
                            await prod_emb.edit(embed=manu_emb)
                        case '🛡':
                            await prod_emb.edit(embed=mil_emb)
                        case _:
                            break
                    await prod_emb.remove_reaction(reaction.emoji, user)

            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

    # Reserve Command
    @commands.command()
    async def reserve(self, ctx):
        user_id = ctx.author.id

        # fetch user nation_name
        cursor.execute('SELECT nation_name FROM user_info WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            nation_name = result[0]

            # fetch user's resources
            cursor.execute(
                'SELECT name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete FROM resources WHERE name = ?',
                (nation_name,))
            resource_result = cursor.fetchone()

            if resource_result:
                name, wood, coal, iron, lead, bauxite, oil, uranium, food, steel, aluminium, gasoline, ammo, concrete = resource_result

                embed=discord.Embed(
                    title=f'{name}\'s Reserves',
                    description='Displays nation\'s national reserves.',
                    color=0x4CAF50)
                embed.add_field(name=f'Wood: {wood:,}', value='', inline=False)
                embed.add_field(name=f'Coal: {coal:,}', value='', inline=False)
                embed.add_field(name=f'Iron: {iron:,}', value='', inline=False)
                embed.add_field(name=f'Lead: {lead:,}', value='', inline=False)
                embed.add_field(name=f'Bauxite: {bauxite:,}', value='', inline=False)
                embed.add_field(name=f'Oil: {oil:,}', value='', inline=False)
                embed.add_field(name=f'Uranium: {uranium:,}', value='', inline=False)
                embed.add_field(name=f'Food: {food:,}', value='', inline=False)
                embed.add_field(name=f'Steel: {steel:,}', value='', inline=False)
                embed.add_field(name=f'Aluminium: {aluminium:,}', value='', inline=False)
                embed.add_field(name=f'Gasoline: {gasoline:,}', value='', inline=False)
                embed.add_field(name=f'Ammo: {ammo:,}', value='', inline=False)
                embed.add_field(name=f'Concrete: {concrete:,}', value='', inline=False)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                      description=f'Cannot find stats.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(colour=0xEF2F73, title="Error", type='rich',
                                  description=f'You do not have a nation.{new_line}'
                                              f'To create one, type `$create`.')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Production(bot))