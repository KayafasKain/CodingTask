CNXION Coding Task
==================

This is CNXION coding task.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django

The task
========

Summary
-------
Your task is to create a django model that would store any data (based on a priori defined data scheme) and make this model usable across the project (admin integration + simple form view for adding new instances).

Solution
--------
Please create a separate branch where you can commit your work. Follow general guidelines of keeping git history clean and use meaningful messages. Please submit your solution as an open pull request to this repository.

Please describe your solution in the seperate paragraph at the bottom of this README file. Description should contain information like: solution overview, basic details, reasons for choosing one approach vs others. `A picture is worth a thousand words` - so any screenshots explaining the solution or showing it works are appreciated.

Requirements
------------
- django model, say `GenericModel`, that stores any data (proposed aproach is to use JSON field but we're open to better solutions)
- come up with a scheme describing data that `GenericModel` can store/process, for simplicity let's store it as a project-wide setting. Scheme can support only basic data types, like number, strings etc.
- view with form for end users for adding new instances of the `GenericModel` with appropriate validation. Example: if scheme declares we have "age" field that is of "integer" type and "name" field that is of "string" type, the form should contain these 2 fields (inputs). If scheme contains 3 fields of "string" type, the form should contain 3 appropriately named inputs etc. Putting text in the form field will cause validation error with relevant message for end users
- django admin integration so admin can view/edit `GenericModel` instances

How to set up this project?
===========================
The project has been built using cookiecutter-django template (https://github.com/pydanny/cookiecutter-django). Please refer to its docs for more information. Launching the project follows well known guidelines of setting up a standard django project:

- creating virtualenv
- installing requirements (local.txt)
- running migrations
- running django dev server

Questions
=========
**Q:** In my opinion, the optimal solution, in this case, is the usage of JSONField because JSON support exists in some DBMS, and this fact allows to search by them and additionally it could be easily modified. As an alternative - using at least two models instead of one. The first model to define the object, while the second one is being implemented as key/value with the reference to the object. In the latest case the cons is that we get the entity, that doesn't provide an object in fact. 

**A:** The latter approach (using 2 models) I think it's not the best here, because if a model has lots of fields you'd need fetch lots of models to just have one entity. And if you're going to iterate over let's say 100 objects where each model has 100 fields then you have 10 000 DB reads to just fetch 100 entities.

**Q:** May I use additional solutions like https://marshmallow.readthedocs.io/en/latest/ or http://docs.python-cerberus.org/en/stable/?

**A:** Yep, feel free to use additional solutions and libraries like marshmallow. However not sure if it's not limiting us from having truly generic structure? Marshmallow needs to have Schema class created. Not sure how are you going to have this class working if the schema inside needs to be dynamic (based on configuration)? One way is metaclasses but it's not worth the effort I guess unless you really understsand metaclasses in Python.

**Q:** How is the schema defined? What I mean is your vision of how it should be defined, stored and served? It could be defined by code, like classes as in marshmallow or being stored in a text file next to the code or just be stored in the DB. The decision here strongly depends on the use case and it is not obvious as the task is synthetic. I would recommend marshmallow approach, that will allow solving migration questions, though other approaches are more flexible.

**A:** So how to define the schema is a task itself. It's up to you. Though the readme says:
"come up with a scheme describing data that GenericModel can store/process, for simplicity let's store it as a project-wide setting." so I guess the answer is to store it as a project-wide setting.
Example: python dict that describes fields/types etc.

**Q:** Access to attributes should be like `GenericModelInstance.age`?

**A:**  Doesn't matter, as you wish. Let's not invent new requirements, and keep the task simple. The goal of the task is to do:

* Django model that stores any data
* scheme
* view with a working form
* Django admin integration so admin can edit the instances somehow

**Q:** Do we need to support null and/or default values for GenericModel? Should data stored in model be always initialized with a value or necessary to support null, for example for optional settings?

**A:** Good question. For the sake of simplicity let's assume all attributes are optional

**Q:** How to handle changes in the pre-defined schema? Are migrations necessary?

**A:** No, no migrations are necessary. There's only a form for adding new instances, so if the scheme changes, the form for adding new objects should also be changed. But that doesn't touch previously added objects.

**Q:** How should it be displayed for the user and for the admin in the admin panel? From my understanding, there should be an option to edit each field like it is model attribute

**A:** Whatever is most simple and quick. It might look bad in terms of UI but functionally it should be working.

**Q:** Do we need to store the references to other objects?

**A:** Good question. Let's assume "no" for the time being.

**Q:** What conventions should be kept?

**A:** Let's assume it should follow standard Python conventions like: be PEP-8 complaint, follow The Zen of Python: https://www.python.org/dev/peps/pep-0020/ In broader sense it should follow well known software principles like SOLID, KISS, DRY etc.


Solution
========

DB/model selection
------------------

My first thought was to use Mongodb, since this database is build to use document-oriented model, which is extremely flexible unlike relational. Yet, i had to take into account such things as standart Django ORM and task conditions, which, for my oppinion, was quite certain about desirable data model.

So, it was decided to use a Potsgres as RDBMS, for a following reasons:

* I had an expirience with postgres
* Posthres supports JSON fields

Django model
------------

The model consists of following fields:

* id - unique record identifier
* data - json field, to store the data

Solution explanation
--------------------

In order to make Django form meet requirements i had to override several methods:

* __init__ - these where the magic happens, at least for the regular form. In these method i am specifying new fields by looping over the list of dictionaries, which contains information about desirable fields (you can find `FLEXIBLE_FORM` in `base` settings). Default values are also getting assigned here.
* save - redefined, in order to adapt data from `flexible fields` to format, known to the database.

I also had to redefine `get_fields` method from GenericModelAdmin in similar way to `__init__` from `FlexibleForm`,  it was necesserry in order to make `flexible fields` appear in admin interface.

Model-level validation is also provided, by comparing expected field types and actual. Valiation itself happens in redefined `save` method of the model.