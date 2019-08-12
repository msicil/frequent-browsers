import graphene
from graphene_django import DjangoObjectType
from django.db import connection

from frequentbrowsers.models import Sites, People, Visits, FrequentBrowsers


class SitesType(DjangoObjectType):
    class Meta:
        model = Sites


class CreateSite(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()

    class Arguments:
        url = graphene.String()

    def mutate(self, info, url):
        site = Sites(url=url)
        site.save()

        return CreateSite(
            id=site.id,
            url=site.url,
        )


class PeopleType(DjangoObjectType):
    class Meta:
        model = People


class CreatePeople(graphene.Mutation):
    id = graphene.Int()
    first_name = graphene.String()
    last_name = graphene.String()

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()

    def mutate(self, info, first_name, last_name):
        people = People(first_name=first_name, last_name=last_name)
        people.save()

        return CreatePeople(
            id=people.id,
            first_name=people.first_name,
            last_name=people.last_name
        )


class VisitType(DjangoObjectType):
    class Meta:
        model = Visits


class CreateVisit(graphene.Mutation):
    person = graphene.Field(PeopleType)
    site = graphene.Field(SitesType)

    class Arguments:
        personid = graphene.Int()
        siteid = graphene.Int()

    def mutate(self, info, personid, siteid):
        person = People.objects.filter(id=personid).first()
        if not person:
            raise Exception('Invalid Person!')
        site = Sites.objects.filter(id=siteid).first()
        if not site:
            raise Exception('Invalid Site!')
        Visits.objects.create(person=person, site=site)
        return CreateVisit(person=person, site=site)


class FrequentBrowserType(DjangoObjectType):
    class Meta:
        model = FrequentBrowsers


class RefreshFrequentBrowsers(graphene.Mutation):

    frequentBrowsers = graphene.List(FrequentBrowserType)
    message = graphene.String()

    def mutate(self, info):
        cursor = connection.cursor()
        cursor.execute('DELETE FROM frequent_browsers')
        cursor.execute('''INSERT INTO frequent_browsers
        SELECT personId, COUNT(*) AS VisitCount FROM VISITS
        GROUP BY personId
        ORDER BY VisitCount DESC
        LIMIT 10''')
        return RefreshFrequentBrowsers(frequentBrowsers=FrequentBrowsers.objects.all(), message='Frequent Browsers Updated')


class Query(graphene.ObjectType):
    people = graphene.List(PeopleType)
    sites = graphene.List(SitesType)
    frequentBrowsers = graphene.List(FrequentBrowserType)

    def resolve_people(self, info, **kwargs):
        return People.objects.all()

    def resolve_sites(self, info, **kwargs):
        return Sites.objects.all()

    def resolve_frequentBrowsers(self, info, **kwargs):
        return FrequentBrowsers.objects.all()


class Mutation(graphene.ObjectType):
    create_site = CreateSite.Field()
    create_people = CreatePeople.Field()
    create_visit = CreateVisit.Field()
    refresh_frequent = RefreshFrequentBrowsers.Field()
