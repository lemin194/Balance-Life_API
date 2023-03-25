

class Meal(models.Model):
    title = models.CharField(max_length=50)
    time = models.DateTimeField()
    food_list = models.ManyToManyField(Food)
    def __str__(self):
        return self.time.strftime('%Y-%m-%d %H:%M')