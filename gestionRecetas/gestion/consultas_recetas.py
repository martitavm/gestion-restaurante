# 1. Saving ForeignKey y ManyToManyField Fields
# Crea un chef llamado "Gordon Ramsay" con la especialidad "Cocina francesa".

gordon_ramsay = Chef.objects.create(name="Gordon Ramsay", specialty="Cocina francesa")

# Crea una receta llamada "Beef Wellington" con un tiempo de preparación de 120 minutos, creada por "Gordon Ramsay".

beef_wellington = Recipe.objects.create(title="Beef Wellington", preparation_time=120, chef=gordon_ramsay)

# Añade esta receta a dos restaurantes: "Hell's Kitchen" en Londres y "The Savoy Grill" también en Londres.

hells_kitchen = Restaurant.objects.create(name="Hell's Kitchen", location="Londres")
savoy_grill = Restaurant.objects.create(name="The Savoy Grill", location="Londres")

beef_wellington.restaurants.add(hells_kitchen, savoy_grill)

# 2. QuerySets are Lazy

recipes = Recipe.objects.filter(title__icontains="Beef")
# No se ejecuta la consulta en este momento

# Convierte el QuerySet en una lista y observa cuándo se ejecuta:

recipes_list = list(recipes)

# Modifica el QuerySet para ordenar los resultados por tiempo de preparación. ¿El QuerySet inicial se ejecuta otra vez?

recipes_sorted = recipes.order_by("preparation_time")
# Esto crea un nuevo QuerySet, pero la consulta solo se ejecutará cuando se itere sobre él

# 3. Field Lookups
# Encuentra recetas cuyo tiempo de preparación esté entre 30 y 90 minutos.

recetas_entre_30_90 = Recipe.objects.filter(preparation_time__range=(30, 90))

# Busca recetas cuyo título comience con "Chocolate".

recetas_chocolate = Recipe.objects.filter(title__startswith="Chocolate")

# Excluye recetas creadas por chefs con especialidad en "Cocina francesa".

recetas_no_francesas = Recipe.objects.exclude(chef__specialty="Cocina francesa")

# 4. Lookups that Span Relationships
# Encuentra todas las recetas disponibles en restaurantes ubicados en Londres.

recetas_en_londres = Recipe.objects.filter(restaurants__location="Londres").distinct()

# Lista los chefs que tienen al menos una receta disponible en "Hell's Kitchen".

chefs_en_hells_kitchen = Chef.objects.filter(recipe__restaurants__name="Hell's Kitchen").distinct()

# Filtra restaurantes que tienen más de 5 recetas en su menú.

restaurantes_con_mas_5_recetas = Restaurant.objects.annotate(num_recipes=models.Count("recipe")).filter(num_recipes__gt=5)

# 5. F Expressions
# Filtra recetas que tienen más opiniones positivas que pedidos totales (un caso improbable para comprobar lógica).

recetas_con_mas_reviews_pedidos = RecipeStats.objects.filter(positive_reviews__gt=F("total_orders"))

# Incrementa el número de pedidos totales para todas las recetas en 10.

RecipeStats.objects.update(total_orders=F("total_orders") + 10)

# Calcula el porcentaje de opiniones positivas para cada receta.

recetas_porcentaje = RecipeStats.objects.annotate( positive_review_percentage=(F("positive_reviews") * 100.0) / F("total_orders"))

# 6. Querying JSONField

# Inserta una configuración para "Hell's Kitchen" con el siguiente JSON:

# Obtenemos el restaurante "Hell's Kitchen"

hells_kitchen = Restaurant.objects.get(name="Hell's Kitchen")

# Creamos la configuración JSON

config_data = {
    "opening_hours": {"weekdays": "12pm-11pm", "weekends": "10am-11pm"},
    "services": ["delivery", "takeaway", "dine-in"],
    "restricted_dishes": {"alcohol": True, "pork": False}
}

restaurant_config, created = RestaurantConfig.objects.get_or_create(
    restaurant=hells_kitchen,
    defaults={"settings": config_data}
)

# Filtra configuraciones donde el servicio "delivery" esté disponible.

configs_con_delivery = RestaurantConfig.objects.filter(settings__services__contains=["delivery"])

# Encuentra configuraciones donde los platos con alcohol estén restringidos.

configs_sin_alcohol = RestaurantConfig.objects.filter(settings__restricted_dishes__alcohol=True)

# Consulta configuraciones con horarios de fin de semana que comiencen a las "10am".

configs_finde_10am = RestaurantConfig.objects.filter(settings__opening_hours__weekends="10am-11pm")


# Encuentra configuraciones que ofrezcan más de dos servicios.
configs_mas_dos_servicios = RestaurantConfig.objects.annotate(num_services=Func(F("settings__services"), function="jsonb_array_length")).filter(num_services__gt=2)
