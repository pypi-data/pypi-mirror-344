.. _label-results:

Results
=======

After performing an analysis on a reinforced concrete cross-section (see
:ref:`label-analysis`), ``concreteproperties`` provides the user with a results object
specific to the conducted analysis. These results objects have methods tailored for the
post-processing of analysis results.

Gross Area Properties
---------------------

Gross area properties can be retrieved by calling the
:meth:`~concreteproperties.concrete_section.ConcreteSection.get_gross_properties`
method.

..  automethod:: concreteproperties.concrete_section.ConcreteSection.get_gross_properties
  :noindex:

This method returns a :class:`~concreteproperties.results.GrossProperties` object,
which stores all the calculated section properties as attributes. The gross area
properties can be printed to the terminal by calling the
:meth:`~concreteproperties.results.GrossProperties.print_results` method.

..  autoclass:: concreteproperties.results.GrossProperties()
  :noindex:
  :members:

Transformed gross area properties can be obtained by calling the
:meth:`~concreteproperties.concrete_section.ConcreteSection.get_transformed_gross_properties`
method.

..  automethod:: concreteproperties.concrete_section.ConcreteSection.get_transformed_gross_properties
  :noindex:

This method returns a :class:`~concreteproperties.results.TransformedGrossProperties`
object, which stores all the calculated transformed section properties as class
attributes. The transformed gross area properties can be printed to the terminal by
calling the
:meth:`~concreteproperties.results.TransformedGrossProperties.print_results` method.

..  automethod:: concreteproperties.results.TransformedGrossProperties.print_results()
  :noindex:

.. seealso::
  For an application of the above, see the example
  :ref:`/examples/area_properties.ipynb`.


Cracked Area Properties
-----------------------

Performing a cracked analysis with
:meth:`~concreteproperties.concrete_section.ConcreteSection.calculate_cracked_properties`
returns a :class:`~concreteproperties.results.CrackedResults` object.

..  autoclass:: concreteproperties.results.CrackedResults()
  :noindex:
  :members:

.. note::

  A :class:`~concreteproperties.prestressed_section.PrestressedSection` object will
  return a ``tuple`` for the cracking moment ``m_cr``, with the first value the cracking
  moment for positive bending and the second value the cracking moment for negative
  bending.

Calling
:meth:`~concreteproperties.results.CrackedResults.calculate_transformed_properties`
on a :class:`~concreteproperties.results.CrackedResults` object stores the transformed
cracked properties as attributes within the current object.

.. seealso::
  For an application of the above, see the example
  :ref:`/examples/cracked_properties.ipynb`.


Moment Curvature Analysis
-------------------------

Running a
:meth:`~concreteproperties.concrete_section.ConcreteSection.moment_curvature_analysis`
returns a :class:`~concreteproperties.results.MomentCurvatureResults` object. This
object can be used to plot moment curvature results.

..  autoclass:: concreteproperties.results.MomentCurvatureResults()
  :noindex:
  :members: plot_results, plot_multiple_results, plot_failure_geometry, get_curvature

.. seealso::
  For an application of the above, see the example
  :ref:`/examples/moment_curvature.ipynb`.


Ultimate Bending Capacity
-------------------------

The
:meth:`~concreteproperties.concrete_section.ConcreteSection.ultimate_bending_capacity`
method returns an :class:`~concreteproperties.results.UltimateBendingResults` object.
This object stores results relating to the analysis and allows the results to be printed
to the terminal by calling the
:meth:`~concreteproperties.results.UltimateBendingResults.print_results` method.

..  autoclass:: concreteproperties.results.UltimateBendingResults()
  :noindex:
  :members:

.. seealso::
  For an application of the above, see the example
  :ref:`/examples/ultimate_bending.ipynb`.


Moment Interaction Diagram
--------------------------

Calling the
:meth:`~concreteproperties.concrete_section.ConcreteSection.moment_interaction_diagram`
method returns a :class:`~concreteproperties.results.MomentInteractionResults` object.
This object can be used to plot moment interaction results.

..  autoclass:: concreteproperties.results.MomentInteractionResults()
  :noindex:
  :members: plot_diagram, plot_multiple_diagrams, point_in_diagram, get_results_lists

.. seealso::
  For an application of the above, see the example
  :ref:`/examples/moment_interaction.ipynb`.


Biaxial Bending Diagram
-----------------------

The
:meth:`~concreteproperties.concrete_section.ConcreteSection.biaxial_bending_diagram`
method returns a :class:`~concreteproperties.results.BiaxialBendingResults` object.
This object can be used to plot biaxial bending results.

..  autoclass:: concreteproperties.results.BiaxialBendingResults()
  :noindex:
  :members: plot_diagram, plot_multiple_diagrams_2d, plot_multiple_diagrams_3d, point_in_diagram, get_results_lists

.. seealso::
  For an application of the above, see the example
  :ref:`/examples/biaxial_bending.ipynb`.


Stress Analysis
---------------

Stress analyses can be performed by calling any of the following methods:
:meth:`~concreteproperties.concrete_section.ConcreteSection.calculate_uncracked_stress`,
:meth:`~concreteproperties.concrete_section.ConcreteSection.calculate_cracked_stress`,
:meth:`~concreteproperties.concrete_section.ConcreteSection.calculate_service_stress`
and
:meth:`~concreteproperties.concrete_section.ConcreteSection.calculate_ultimate_stress`.
All these methods return a :class:`~concreteproperties.results.StressResult` object.
This object stores results relating to the stress analysis and can also be used to plot
stress results.

..  autoclass:: concreteproperties.results.StressResult()
  :noindex:
  :members:

.. seealso::
  For an application of the above, see the example
  :ref:`/examples/stress_analysis.ipynb`.


Units
-----

Most of the above methods take an optional ``units`` argument as a
:class:`~concreteproperties.post.UnitDisplay()` object. This argument allows results to
be scaled and unit labels applied to numbers/plot axes.

..  autoclass:: concreteproperties.post.UnitDisplay()
  :noindex:

For example, if the model data is specified in ``[N]`` and ``[mm]``, results can be
expressed using ``[kN]`` and ``[m]`` by creating an appropriate ``UnitDisplay`` object:

.. code-block:: python

  from concreteproperties.post import UnitDisplay

  kn_m = UnitDisplay(
    length="m", force="kN", mass="kg", length_factor=1e3, force_factor=1e3
  )

Note that stresses will automatically be displayed as kilopascals using the above
unit system as ``[kPa]`` is equivalent to |kpa|. Similarly, results in ``[N.mm]``,
``[MPa]`` etc. can be automatically displayed by creating a ``UnitDisplay`` object that
represents the base unit system:

.. |kpa| raw:: html

  <code class="docutils literal notranslate"><span class="pre">[kN/m<sup>2</sup>]</span></code>

.. code-block:: python

  from concreteproperties.post import UnitDisplay

  n_mm = UnitDisplay(length="mm", force="N", mass="kg")

Note that the above two unit systems are baked into ``concreteproperties`` in the
``post`` module with the ``si_n_mm`` and ``si_kn_m`` objects:

.. code-block:: python

  from concreteproperties.post import si_kn_m, si_n_mm

``concreteproperties`` welcomes the contribution of further unit systems!
