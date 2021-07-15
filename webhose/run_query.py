from response import search_and_write

params = (
    ('format', 'json'),
    ('sort', 'published'),
    ('q', 'hacking OR malware OR "data breach" OR DDos OR botnet'),
    ('ts', '1533092324961')
)

search_and_write(params)