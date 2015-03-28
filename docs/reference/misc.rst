Miscellaneous
==============

User contributed recipes
~~~~~~~~~~~~~~~~~~~~~~~~

**How to hide a field on a schema if we do not want to or cannot modify the original schema**

To do this one can use tagged values on the schema. In this case want to hide 'introduction' and 'answers' fields:

.. code-block:: python

    from example.package.content.assessmentitem import IAssessmentItem
    from plone.autoform.interfaces import OMITTED_KEY
    IAssessmentItem.setTaggedValue(OMITTED_KEY,
                               [(Interface, 'introduction', 'true'),
                                (Interface, 'answers', 'true')])


This code can sit in another.package.__init__.py for example.

See also: `Original thread on coredev mailinglist`_

.. _Original thread on coredev mailinglist: http://plone.293351.n2.nabble.com/plone-autoform-why-use-tagged-values-td7560956.html
