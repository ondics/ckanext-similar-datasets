ckanext-similar-datasets
#################

*ckanext-similar-datasets* ist eine CKAN_ Extension und fügt eine Liste ähnlicher Datensätze bei der Datensatz-Detailsicht. 

*ckanext-similar-datasets* war ursprünglich Teil des größeren ckanext-discovery_ Plugins und kann jetzt als eigenständiges Plugin genutzt werden.

.. image:: doc/similar_datasets.png
    :alt: Screenshot of the similar_datasets plugin

This Repo currently is only in german language available. Feel free to submit translations.

System-Voraussetzungen
======================

Getestet wurde das Plugin mit CKAN 2.9

Andere Versionen wurden nicht getestet. Feedback zur Funktionalität mit anderen Versionen sind herzlich Willkommen.

Installation
============

Aktivieren der CKAN-Umgebung::

    . /usr/lib/ckan/default/bin/activate

Installation des Plugins::

    pip install -e git+https://github.com/ondics/ckanext-similar-datasets#egg=ckanext-similar-datasets

Zur Installation einer bestimmten Version::

    pip install -e git+https://github.com/ondics/ckanext-similar-datasets@v0.1.1#egg=ckanext-similar-datasets

Funktionsweise
==============

Das Plugin nutzt das SOLR_ `More Like This`_ Feature. Solr muss etwas erweitert werden: 

Der MoreLikeThisHandler_ ist in  ``/etc/solr/conf/solrconfig.xml`` einzurichten.

Dazu den Code Block  direkt vor dem ``</config>`` Tag am Ende der Datei einbauen::

    <requestHandler name="/mlt" class="solr.MoreLikeThisHandler">
        <lst name="defaults">
            <int name="mlt.mintf">3</int>
            <int name="mlt.mindf">1</int>
            <int name="mlt.minwl">3</int>
        </lst>
    </requestHandler>

Weitere Infos zum MoreLikeThisHandler_ für die Konfigurationsdetails.

Zusätzlich muss `term vector storage`_ für das ``text`` Feld in ``/etc/solr/conf/schema.xml`` aktiviert werden. 

In dieser Zeile::

    <field name="text" type="text" indexed="true" stored="false" multiValued="true" />

muss ``termVectors="true"`` ergänzt werden::

    <field name="text" type="text" indexed="true" stored="false" multiValued="true" termVectors="true" />

Hinweis: term vectors vergrößert Größe des Solr Index erheblich.

Dann Neustart von Solr::

    sudo service jetty restart

Zum Schluss sind die Datensätze noch einmalig neu zu indexieren, damit die Term Vektoren der bereits existierenden Datensätzen aufgenommen werden (zukünftige Datensätze werden automatisch hinzugefügt)::

    . /usr/lib/ckan/default/bin/activate
    ckan -c /etc/ckan/default/ckan.ini search-index rebuild

Zum Schluss ``similar-datasets`` zur Liste aktiver Plugins in der CKAN Konfigurations INI hinzufügen::
    
    plugins = ... similar_datasets

und  CKAN neu starten::

    sudo service apache2 restart

oder::

    sudo supervisorctl restart ckan-uwsgi:


Konfiguration
-------------
Das Plugin bietet eine zusätzliche Einstellung an, die in der CKAN Konfigurationsdatei hinzugefügt und angepasst werden kann::

    # Die maximale Anzahl an ähnlichen Datensätzen die gelistet werden können. Default ist 5.
    ckanext.similar_datasets.max_num = 5
    
Credits
=======

Dank geht an die Repo-Ersteller

    CKAN_
    SOLR_
    ckanext-discovery_
    

Lizenz
=======

Distributed in der the GNU Affero General Public License. 

See the file ``LICENSE`` for details.

Autor
=====

Copyright (C) 2021 Ondics GmbH

https://ondics.de



.. _CKAN: https://ckan.org
.. _SOLR: https://solr.apache.org/
.. _configuration INI: https://docs.ckan.org/en/latest/maintaining/configuration.html#ckan-configuration-file
.. _package_search: https://docs.ckan.org/en/latest/api/index.html#ckan.logic.action.get.package_search
.. _More Like This: https://cwiki.apache.org/confluence/display/solr/MoreLikeThis
.. _MoreLikeThisHandler: https://cwiki.apache.org/confluence/display/solr/MoreLikeThis#MoreLikeThis-ParametersfortheMoreLikeThisHandler
.. _term vector storage: https://cwiki.apache.org/confluence/display/solr/Field+Type+Definitions+and+Properties#FieldTypeDefinitionsandProperties-FieldDefaultProperties
.. _template snippet: http://docs.ckan.org/en/latest/theming/templates.html#snippets
.. _ckanext-discovery: https://github.com/stadt-karlsruhe/ckanext-discovery
