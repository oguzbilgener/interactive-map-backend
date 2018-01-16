from django.db.models import Model, TextField, DateField, ForeignKey, ManyToManyField, CASCADE, SET_NULL
# Never use Charfield. Always use TextField. Postgres treats them the same anyways
# from django.contrib.gis.db.models import PolygonField


class State(Model):
    """
    A State is any cultural/governmental entity that we want to draw on the map.
    It will serve as the foreign key for most other objects.
    We'll start off with a minimal set of fields, we can easily add more if necessary.
    """
    # TODO: Do we want to get rid of aliases and make names their own model?
    # It depends on how we wish to handle state discontinuities like government/name changes.
    # e.g. Do we want to call France something different from 1789-1805? Do we want the Roman Empire
    # to live on as the Byzantine? Am I overthinking this?
    # TODO: On the other end of the spectrum, should we make 'name' the primary key? This could be
    # our desired unique identifier
    name = TextField(help_text='Canonical name -- each state should have only one.')
    aliases = TextField(help_text='Other names this state may be known by.', null=True, blank=True)
    # TODO: Do we need an internal unique country_id for every State? (IMO no)
    # Requiring it would be laborious and cumbersome (we need a consistent hashing schema, and conflict
    # resolution may be controversial). On the other hand, it may be helpful to handle states that
    # go through many name changes
    # country_id = TextField(primary_key=True, help_text='Internal country code for unique internal identification')
    description = TextField(help_text='Links, flavor text, etc.', null=True, blank=True)
    color = TextField(help_text='I expect this to be the most controversial field.')

    def __str__(self):
        return self.name


class Event(Model):
    """
    An Event is a date associated with some flavor text and optionally the States affected.
    It may be further associated with a border change via the start_event and end_event in Shapes
    """
    name = TextField(help_text='Canonical name of the event')
    date = DateField()
    states = ManyToManyField(State, help_text='State(s) affected by this event.')
    description = TextField(help_text='Flavor text, Wikipedia, etc.', null=True, blank=True)

    def __str__(self):
        return f'{self.name}: {self.date}'


class Shape(Model):
    """
    A Shape is a region polygon associated with a State from a start_date to an end_date.
    This should accomodate States with discontiguous territories and existences.
    A Shape may optionally have Events attached to its start_date and end_date.
    """
    state = ForeignKey(State, on_delete=CASCADE)
    # TODO: Figure out the right way to store the shapefile here. PolygonField feels like the right approach, but is it?
    # Progress! It will probably involve LayerMapping (https://docs.djangoproject.com/en/2.0/ref/contrib/gis/layermapping/)
    # TODO: Add this field once this app is dockerized and Postgres + PostGIS are working
    # shape = PolygonField()
    start_date = DateField(help_text='When this border takes effect.')
    start_event = ForeignKey(Event, on_delete=SET_NULL, null=True, blank=True, related_name='start_event')
    end_date = DateField(help_text='When this border ceases to exist.')
    end_event = ForeignKey(Event, on_delete=SET_NULL, null=True, blank=True, related_name='end_event')

    def __str__(self):
        return f'{self.state}: {self.start_date} to {self.end_date}'
