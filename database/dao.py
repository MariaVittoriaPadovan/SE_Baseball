from database.DB_connect import DBConnect
from model.team import Team


class DAO:

    @staticmethod
    def get_years_from_1980():
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT DISTINCT year
                FROM team
                WHERE year >= 1980
                ORDER BY year
                """

        try:
            cursor.execute(query)
            for row in cursor:
                result.append(row['year'])

        except Exception as e:
            print("Errore durante la query year")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di years

    @staticmethod
    def get_teams_by_year(year):
        cnx = DBConnect.get_connection()
        result = []

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT id, team_code, name
                FROM team
                WHERE year = %s
                """

        try:
            cursor.execute(query, (year,))
            for row in cursor:
                result.append(Team(row['id'], row['team_code'], row['name']))

        except Exception as e:
            print("Errore durante la query squadre per anno")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # lista di oggetti Team

    @staticmethod
    def get_team_salary(year):
        cnx = DBConnect.get_connection()
        result = {} #dizionario con chiave team_id e valore salario totale

        if cnx is None:
            print("Connection failed")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = """
                SELECT team_id, SUM(salary) as total
                FROM salary
                WHERE year = %s
                GROUP BY team_id
                """

        try:
            cursor.execute(query, (year,))
            for row in cursor:
                result[row['team_id']] = row['total']

        except Exception as e:
            print("Errore durante la query salario")
            result = None
        finally:  # fa quello che scrivo sia che vado nel try sia che vado nell'except
            cursor.close()
            cnx.close()

        return result  # dizionario team_id : totale