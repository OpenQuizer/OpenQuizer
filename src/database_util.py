import os
import psycopg2


class Database(object):
    """
    This class maintains all about data exchanging.
    """
    def __init__(self):
        DATABASE_URL = os.environ['DATABASE_URL']
        self.conn    = psycopg2.connect(DATABASE_URL, sslmode='require')

    def get_DBver(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT VERSION()')
        results = cursor.fetchall()
        cursor.close()
        return results

    def insert_article(self, title: str, textual_c=0, textual_f=0,
            bgk_c=0, bgk_f=0, ans_num=0, e_score=0.0, unique_visits=0, shares=0, visits=0):
        '''
        Insert data to 'articles' table.
        Args:
            [title, {textual_c, textual_f, bgk_c, bgk_f, ans_num, 
            e_score, unique_visits, shares, visits}]: Data of an article to insertion.
        Return:
            article_id(int): id respective to inserted article.
        '''
        cursor = self.conn.cursor()
        cursor.execute(f'''INSERT INTO articles 
            (title, textual_c, textual_f, bgk_c, bgk_f, ans_num, e_score, unique_visits, shares, visits)
            VALUES ('{title}', {textual_c}, {textual_f}, {bgk_c}, {bgk_f}, {ans_num}, {e_score}, 
            {unique_visits}, {shares}, {visits})
            RETURNING id;''')
        article_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return article_id

    def update_article_by_id(self, id:int, data:dict):
        try:
            cursor = self.conn.cursor()
            update = ''
            for k,v in data.items():
                if type(v) == str:
                    v = f'\'{v}\''
                if update != '':
                    update += ','
                update += f'{k}={v}'
            sql = f'''UPDATE articles SET {update} WHERE id={id};'''
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
        except:
            self.__del__()

    def update_article_by_title(self, title:str, data:dict):
        try:
            cursor = self.conn.cursor()
            update = ''
            for k,v in data.items():
                if type(v) == str:
                    v = f'\'{v}\''
                if update != '':
                    update += ','
                update += f'{k}={v}'
            sql = f'''UPDATE articles SET {update} WHERE title={title};'''
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
        except:
            self.__del__()

    def get_article_by_id(self, id:int):
        '''
        Get data from 'articles' table.
        Args:
            id(int): article index.
        Return:
            data(dict): [{'key': 'data', ...}
        '''
        try:
            keys = ('id', 'title','textual_c','textual_f','bgk_c','bgk_f','ans_num','e_score','unique_visits','shares','visits')
            cursor = self.conn.cursor()
            cursor.execute(f'SELECT * from articles WHERE id={id};')
            data = cursor.fetchone()
            data = zip(keys,data)
            cursor.close()
            return {k:v for k,v in data}
        except:
            self.__del__()
        return None

    def get_article_by_title(self, title:str):
        '''
        Get data from 'articles' table.
        Args:
            id(int): article index.
        Return:
            data(dict): [{'key': 'data', ...}
        '''
        try:
            keys = ('id','title','textual_c','textual_f','bgk_c','bgk_f','ans_num'
                ,'e_score','unique_visits','shares','visits')
            cursor = self.conn.cursor()
            cursor.execute(f'SELECT * from articles WHERE title=\'{title}\';')
            data = cursor.fetchone()
            data = zip(keys,data)
            cursor.close()
            return {k:v for k,v in data}
        except:
            self.__del__()
        return None

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    # print(f"Database version: {db.get_DBver()}")
    # id = db.insert_article('test_article')
    # print(f'insert id: {id}')
    # db.get_article_by_id(1)
    db.update_article_by_id(1, {'title':'test_article_test'})
    print(db.get_article_by_id(1))


'''
CREATE TABLE public.articles
(
    "id" serial,
    title text NOT NULL,
    textual_c integer,
    textual_f integer,
    bgk_c integer,
    bgk_f integer,
    ans_num integer,
    e_score real,
    unique_visits integer,
    shares integer,
    visits integer,
	PRIMARY KEY ("id")
)
TABLESPACE pg_default;

ALTER TABLE public.articles
    OWNER to dlfxsoyfdxhsoz;
'''