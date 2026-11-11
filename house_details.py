from mysql import connector


class Dbconnect:
    def get_connection(self):
        try:
            self.connection = connector.connect(
                host="localhost",
                user="root",
                password="YOUR_MYSQL_PASSWORD",
                database="house_db"
            )
            return self.connection
        except Exception as e:
            return None


class House_details(Dbconnect):

    def post(self, **kwargs):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()
 
            query = """
            INSERT INTO house_details
            (owner_name, place, house_type, bedrooms, price)
            VALUES (%s, %s, %s, %s, %s)
            """

            values = [v for v in kwargs.values()]

            self.cursor.execute(query, values)
            self.connect.commit()
            print("New house added successfully")

        except Exception as e:
            print(e)

    def get(self):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()

            query = "SELECT * FROM house_details"
            self.cursor.execute(query)

            records = self.cursor.fetchall()
            return records

        except Exception as e:
            return []

    def get_object(self, id=None):
        try:
            self.connect = super().get_connection()
            self.cursor = self.connect.cursor()

            query = "SELECT * FROM house_details WHERE id = %s"
            values = (id,)

            self.cursor.execute(query, values)
            record = self.cursor.fetchone()

            return record

        except Exception as e:
            print(e)

    def retrieve(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is None:
                print("House not found..!")
            else:
                print(record)

        except Exception as e:
            print(e)

    def delete(self, id=None):
        try:
            record = self.get_object(id=id)

            if record is not None:
                query = "DELETE FROM house_details WHERE id = %s"
                values = (id,)

                self.cursor.execute(query, values)
                self.connect.commit()

                print("House deleted successfully..!")
            else:
                print("House not found..!")

        except Exception as e:
            print(e)

    def put(self, id=None, **kwargs):
        try:
            record = self.get_object(id=id)

            if record is not None:
                self.cursor = self.connect.cursor()

                placeholder = ""

                for k in kwargs.keys():
                    placeholder += k + "=%s,"

                placeholder = placeholder.rstrip(",")

                query = f"UPDATE house_details SET {placeholder} WHERE id = %s"

                values = [v for v in kwargs.values()]
                values.append(id)

                self.cursor.execute(query, values)
                self.connect.commit()

                print("House updated successfully..!")
            else:
                print("House not found..!")

        except Exception as e:
            print(e)


connection_instance = Dbconnect()
print(connection_instance.get_connection())

house_view = House_details()

house_view.post(
    owner_name="Ajith",
    place="Idukki",
    house_type="Villa",
    bedrooms="3",
    price="5000000"
)

house_view.get()

print("_____________________")
house_view.retrieve(1)

print("-------------")
house_view.delete(2)

print("-------------")
house_view.get()

print("-------------")
house_view.put(1, owner_name="Anto", place="Kannur", house_type="Apartment", bedrooms="2", price="3500000")

house_view.retrieve(1)