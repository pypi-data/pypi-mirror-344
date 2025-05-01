# Change log

## 1.3.0

2025-04-30

* Add support for Python 3.12 and 3.13.
* Add support for Django 5.2.
* Drop support for Python 3.8.
* Drop support for Django 3.2.

## 1.2.1

2023-08-27

* Add back support for fields named `model` to `ifactory.create()` and
  `ifactory.configure_defaults()`.
* Fix stack level of deprecation warnings.

## 1.2.0

2023-08-27

* Add support for giving the field values to `ifactory.create()` and
  `ifactory.configure_defaults()` with keyword arguments and deprecate
  the old convention to pass them in a dict.
* Add type annotations and mark the package as typed.
* Drop support for Python 3.7.

## 1.1.0

2023-06-06

* Add explicit support for EmailField.

## 1.0.0

2023-05-21

* Drop support for Django 2.2.
* Add support for Django 4.2.
* Add support for Python 3.10 and 3.11.

## 0.5.0

2022-02-09

* Drop support for Python 3.6.
* Drop support for Django 3.0 and 3.1.
* Add support for Django 3.2.
* Remove Django from the install requirements.  This is in line with
  pytest-django.

## 0.4.0

2021-01-13

* Drop support for Python 3.5 and add support for Python 3.9.
* Add support for Django 3.1.


## 0.3.0

2020-03-08

* Drop support for Python 2.7 and 3.4 and add support for Python 3.8.
* Drop support for Django 2.1 and add support for Django 2.2 and 3.0.
* Move to the Gorilla Development group at GitLab.com.


## 0.2.1

2018-12-20

* Removed an unintenional dependency on libgdal (issue #4).


## 0.2.0

2018-10-28

* Moved repo to gitlab.com and set up CI.
* Documented that there is a transactional_ifactory fixture as well.
* Added support for GeoDjango's geometry fields.


## 0.1.0

2018-08-10

* Initial release.
