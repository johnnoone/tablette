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

        duis autem vel eum iriure dolor in hendrerit in vulputate velit esse
        molestie consequat vel illum dolore eu feugiat nulla facilisis at vero eros
        et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril
        delenit augue duis dolore te feugait nulla facilisi lorem ipsum dolor sit
        amet consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt ut
        laoreet dolore magna aliquam erat volutpat

        ut wisi enim ad minim veniam quis nostrud exerci tation ullamcorper suscipit
        lobortis nisl ut aliquip ex ea commodo consequat duis autem vel eum iriure
        dolor in hendrerit in vulputate velit esse molestie consequat vel illum
        dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio
        dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te
        feugait nulla facilisi

        nam liber tempor cum soluta nobis eleifend option congue nihil imperdiet
        doming id quod mazim placerat facer possim assum lorem ipsum dolor sit amet
        consectetuer adipiscing elit sed diam nonummy nibh euismod tincidunt ut
        laoreet dolore magna aliquam erat volutpat ut wisi enim ad minim veniam quis
        nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea
        commodo consequat

        duis autem vel eum iriure dolor in hendrerit in vulputate velit esse
        molestie consequat vel illum dolore eu feugiat nulla facilisis

        at vero eos et accusam et justo duo dolores et ea rebum stet clita kasd
        gubergren no sea takimata sanctus est lorem ipsum dolor sit amet lorem ipsum
        dolor sit amet consetetur sadipscing elitr sed diam nonumy eirmod tempor
        invidunt ut labore et dolore magna aliquyam erat sed diam voluptua at vero
        eos et accusam et justo duo dolores et ea rebum stet clita kasd gubergren no
        sea takimata sanctus est lorem ipsum dolor sit amet lorem ipsum dolor sit
        amet consetetur sadipscing elitr at accusam aliquyam diam diam dolore
        dolores duo eirmod eos erat et nonumy sed tempor et et invidunt justo labore
        stet clita ea et gubergren kasd magna no rebum sanctus sea sed takimata ut
        vero voluptua est lorem ipsum dolor sit amet lorem ipsum dolor sit amet
        consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore
        et dolore magna aliquyam erat

        consetetur sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore
        et dolore magna aliquyam erat sed diam voluptua at vero eos et accusam et
        justo duo dolores et ea rebum stet clita kasd gubergren no sea takimata
        sanctus est lorem ipsum dolor sit amet lorem ipsum dolor sit amet consetetur
        sadipscing elitr sed diam nonumy eirmod tempor invidunt ut labore et dolore
        magna aliquyam erat sed diam voluptua at vero eos et accusam et justo duo
        dolores et ea rebum stet clita kasd gubergren no sea takimata sanctus est
        lorem ipsum dolor sit amet lorem ipsum dolor sit amet consetetur sadipscing
        elitr sed diam nonumy eirmod tempor invidunt ut labore et dolore magna
        aliquyam erat sed diam voluptua at vero eos et accusam et justo duo dolores
        et ea rebum stet clita kasd gubergren no sea takimata sanctus est lorem
        ipsum dolor sit amet
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
