from sdui_api import classes, wrapper

wrp = wrapper.Wrapper(False, 3600, 305870, -1, "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxMDAwNyIsImp0aSI6ImU4MzMxMjY1ZWQwNTYwODAzOGJmMTVjMjQzNDUxYWRmZmFkNzQwOTE1ZDhjODg0ZDYxNDlkMzA1YWFmMTVmYTlhMzA2MDgzMzlkNGY1ZTM5IiwiaWF0IjoxNjMyMDc4NjQzLCJuYmYiOjE2MzIwNzg2NDMsImV4cCI6MTY2MzYxNDY0Mywic3ViIjoiMzA1ODcwIiwic2NvcGVzIjpbXX0.iIZVqxCz7rcmd-4DF02NBJkSaaxulWkhKTkDA3r9tATeowtntIe2YREtVBpvkV_SlbwGnrJKMuqr_8AvLkbS5ttYR13DUsWi2tlozyuNuueVJL6Yv2pb8FJOyO0RLHklt9CSM_LGkBarg-fA5KmWFOSydIK0lrXQgu1PD8fxCrQubca9FbbzZ5WXMOc4d9JDfmLQHsMTGEoEL4Bti8ZqWVE3cOt6ssXZ5LXHxaJfuJ-nNWPpdMOsCNKjFMv1XA445NZgJtPUkZV0B1rtg2WTh2mntvsDyPscg-VA4hozVEnkIGjdDiCuVxhaTU_dJWVKYGWBy6NGyL4Lhx_ZOBDCGlxk5YmEuRHR17_00bBViqo_Cx4k-6pnw8HMtt7AYDAegJaPeK40mtHUBq0tQkwofb40etog-VP2wGrQ0fWSJYkzy5Xlvw5xcqAixg2jYNZstHhk5-HK5mkqL-JPijvvrX7f2zdTH7hQdDy-7xuL0Zm7y37o3tojhbzl6zU9U74_4sqYXs61IfzQbU-QHq4SiMR7o7d1IOeEt1TQ305eBzbIaR7o0ZReLJrGVq8nq8f424q8BtD7jFhwIrpg-WLm3hlMPUJF0aFSycfNtKGFrhuF7zwpRQUhrLhALXMP2wEw0FH0QTuhsSzPMhPJfDVgjQ1JJfx9n500POqN5bSObuY")

print(wrp.get_lessons_for_day())