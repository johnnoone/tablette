Tablette
========

Print any iterator to table.


For example, this will print this 1000000 rows data, and format the 4th columns::

    from tablette import Tablette


    def data():
        import random

        cities = (
            'Adelaide',
            'Brisbane',
            'Darwin',
            'Hobart',
            'Sydney',
            'Melbourne',
            'Perth',
            'Kuala Lumpur',
        )

        words = sorted(set("""
            lorem ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy
            eirmod tempor invidunt ut labore et dolore magna aliquyam erat sed diam
            voluptua at vero eos et accusam et justo duo dolores et ea rebum stet clita
            kasd gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem
            ipsum dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod
            tempor invidunt ut labore et dolore magna aliquyam erat sed diam voluptua at
            vero eos et accusam et justo duo dolores et ea rebum stet clita kasd
            gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem ipsum
            dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor
            invidunt ut labore et dolore magna aliquyam erat sed diam voluptua at vero
            eos et accusam et justo duo dolores et ea rebum stet clita kasd gubergren no
            sea takimata sanctus est lorem ipsum dolor sit amet
        """.split()))

        sizes = [
            (1, 20),
            (5, 10),
            (10, 30),
            (20, 35),
            (10, 45),
        ]

        size_1 = random.choice(sizes)
        size_2 = random.choice(sizes)
        for i in range(0, 1000000):
            if i % 50 == 0:
                size_1 = random.choice(sizes)
            if i % 40 == 0:
                size_2 = random.choice(sizes)
            city = random.choice(cities)
            area = random.randrange(112, 7000)
            population = random.randrange(20000, 10000000)
            rain = float(random.randrange(5000, 9000)) / 10
            text1 = ' '.join(random.choice(words) for i in range(0, random.randint(*size_1)))
            text2 = ' '.join(random.choice(words) for i in range(0, random.randint(*size_2)))
            yield city, area, population, rain, text1, text2

    yo = Tablette([
        "City name",
        "Area",
        "Population",
        {'name': "Annual Rainfall",
         'term': lambda x: {'color': 'red',
                            'attrs': ['bold']} if x > 800 else None},
        "Note",
        "Note2"
    ], data())
    for row in yo.printer():
        print(row)
