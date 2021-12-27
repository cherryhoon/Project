author = """--sql
        select * from author
        left join author_died
            on author.id = author_died.author_id
        where author.id = :id
        """

author_country = """--sql
        select * from author
        inner join author_country
            on author.id = author_country.author_id
        inner join country
            on country.id = author_country.country_id
        where author.id = :id
        """

item_groups = """--sql
        select category.name as 'category' from author
        inner join author_item
            on author.id = author_item.author_id
        inner join item
            on item.id = author_item.item_id
        inner join category
            on category.id = item.category_id
        where author.id = :id
        group by category.name
        """

author_one_group = """--sql
            select item.name from author
            inner join author_item
                on author.id = author_item.author_id
            inner join item
                on item.id = author_item.item_id
            inner join category
                on category.id = item.category_id
            where author.id = :id and category.name = :category
"""

item = """--sql
        select * from item
        where item.id = :id
    """

item_author = """--sql
        select * from author_item
        inner join author
            on author.id = author_item.author_id
        where author_item.item_id = :id
    """

item_countries = """--sql
        select country.name from author_item
        inner join author
            on author.id = author_item.author_id
        inner join author_country
            on author.id = author_country.author_id
        inner join country
            on country.id = author_country.country_id
        where author_item.item_id = :id
    """

item_category = """--sql
            select item.name, item.id from item
            inner join category
                on category.id = item.category_id
            where category.name = :category
        """
