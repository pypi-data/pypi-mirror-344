# -*- coding: utf-8 -*-
'''
diacamma.pro tests package

@author: Laurent GAY
@organization: sd-libre.fr
@contact: info@sd-libre.fr
@copyright: 2019 sd-libre.fr
@license: This file is part of Lucterios.

Lucterios is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Lucterios is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Lucterios.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import unicode_literals
from shutil import rmtree
import datetime

from lucterios.framework.test import LucteriosTest
from lucterios.framework.filetools import get_user_dir
from lucterios.CORE.parameters import Params
from lucterios.CORE.views import ParamEdit, ParamSave

from diacamma.microbusiness.views import BussinessConf, SocialDeclarationList, SocialDeclarationCalcul
from diacamma.accounting.test_tools import initial_thirds_fr, default_compta_fr, fill_entries_fr
from diacamma.accounting.models import FiscalYear


class AdminTest(LucteriosTest):

    def setUp(self):
        initial_thirds_fr()
        LucteriosTest.setUp(self)
        default_compta_fr()
        rmtree(get_user_dir(), True)

    def test_default_configuration(self):
        self.factory.xfer = BussinessConf()
        self.calljson('/diacamma.microbusiness/bussinessConf', {}, False)
        self.assert_observer('core.custom', 'diacamma.microbusiness', 'bussinessConf')
        self.assert_count_equal('', 1 + 3)

        self.assert_json_equal('LABELFORM', 'microbusiness-sellaccount', '')
        self.assert_json_equal('LABELFORM', 'microbusiness-serviceaccount', '')
        self.assert_json_equal('LABELFORM', 'microbusiness-simple-socialdeclaration', 'Oui')

        self.factory.xfer = ParamEdit()
        self.calljson('/CORE/paramEdit', {'params': 'microbusiness-sellaccount;microbusiness-serviceaccount;microbusiness-simple-socialdeclaration'}, False)
        self.assert_observer('core.custom', 'CORE', 'paramEdit')
        self.assert_json_equal('CHECKLIST', 'microbusiness-sellaccount', [''])
        self.assert_json_equal('CHECKLIST', 'microbusiness-serviceaccount', [''])
        self.assert_json_equal('CHECK', 'microbusiness-simple-socialdeclaration', True)
        self.assert_select_equal('microbusiness-sellaccount', {"701": "[701] 701", "706": "[706] 706", "707": "[707] 707"}, checked=True)
        self.assert_select_equal('microbusiness-serviceaccount', {"701": "[701] 701", "706": "[706] 706", "707": "[707] 707"}, checked=True)

        self.factory.xfer = ParamSave()
        self.calljson('/CORE/paramSave', {'params': 'microbusiness-sellaccount;microbusiness-serviceaccount;microbusiness-simple-socialdeclaration', 'microbusiness-sellaccount': '701', 'microbusiness-serviceaccount': '706', 'microbusiness-simple-socialdeclaration': '1'}, False)
        self.assert_observer('core.acknowledge', 'CORE', 'paramSave')

        self.factory.xfer = BussinessConf()
        self.calljson('/diacamma.microbusiness/bussinessConf', {}, False)
        self.assert_observer('core.custom', 'diacamma.microbusiness', 'bussinessConf')
        self.assert_count_equal('', 1 + 3)
        self.assert_json_equal('LABELFORM', 'microbusiness-sellaccount', '[701] 701')
        self.assert_json_equal('LABELFORM', 'microbusiness-serviceaccount', '[706] 706')
        self.assert_json_equal('LABELFORM', 'microbusiness-simple-socialdeclaration', 'Oui')

        self.factory.xfer = ParamSave()
        self.calljson('/CORE/paramSave', {'params': 'microbusiness-simple-socialdeclaration', 'microbusiness-simple-socialdeclaration': '0'}, False)
        self.assert_observer('core.acknowledge', 'CORE', 'paramSave')

        self.factory.xfer = BussinessConf()
        self.calljson('/diacamma.microbusiness/bussinessConf', {}, False)
        self.assert_observer('core.custom', 'diacamma.microbusiness', 'bussinessConf')
        self.assert_count_equal('', 1 + 1)
        self.assert_json_equal('LABELFORM', 'microbusiness-simple-socialdeclaration', 'Non')


class SocialDeclarationTest(LucteriosTest):

    def setUp(self):
        initial_thirds_fr()
        LucteriosTest.setUp(self)
        default_compta_fr()
        rmtree(get_user_dir(), True)

    def test_nolist(self):
        Params.setvalue('microbusiness-simple-socialdeclaration', False)
        self.factory.xfer = SocialDeclarationList()
        self.calljson('/diacamma.microbusiness/socialDeclarationList', {}, False)
        self.assert_observer('core.exception', 'diacamma.microbusiness', 'socialDeclarationList')
        self.assert_json_equal('', "message", "Mauvaise permission pour ''")

    def test_list(self):
        current_year = datetime.date.today().year
        self.factory.xfer = SocialDeclarationList()
        self.calljson('/diacamma.microbusiness/socialDeclarationList', {}, False)
        self.assert_observer('core.custom', 'diacamma.microbusiness', 'socialDeclarationList')
        self.assert_count_equal('', 4)
        self.assert_json_equal('FLOAT', 'year', current_year)
        self.assert_count_equal('socialdeclaration', 0)

        FiscalYear.objects.create(begin="%s-01-01" % current_year, end="%s-12-31" % current_year)

        self.factory.xfer = SocialDeclarationList()
        self.calljson('/diacamma.microbusiness/socialDeclarationList', {}, False)
        self.assert_observer('core.custom', 'diacamma.microbusiness', 'socialDeclarationList')
        self.assert_json_equal('FLOAT', 'year', current_year)
        self.assert_count_equal('socialdeclaration', 4)

    def test_calcul(self):
        current_year = datetime.date.today().year
        year = FiscalYear.objects.create(begin="%s-01-01" % current_year, end="%s-12-31" % current_year)
        fill_entries_fr(year.id, withyear=True)
        self.factory.xfer = ParamSave()
        self.calljson('/CORE/paramSave', {'params': 'microbusiness-sellaccount;microbusiness-serviceaccount', 'microbusiness-sellaccount': '701', 'microbusiness-serviceaccount': '707'}, False)
        self.assert_observer('core.acknowledge', 'CORE', 'paramSave')

        self.factory.xfer = SocialDeclarationList()
        self.calljson('/diacamma.microbusiness/socialDeclarationList', {}, False)
        self.assert_observer('core.custom', 'diacamma.microbusiness', 'socialDeclarationList')
        self.assert_json_equal('FLOAT', 'year', current_year)
        self.assert_count_equal('socialdeclaration', 4)
        self.assert_json_equal('', 'socialdeclaration/@0/id', 1)
        self.assert_json_equal('', 'socialdeclaration/@0/quarter', 1)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_other', 0)
        self.assert_json_equal('', 'socialdeclaration/@1/id', 2)
        self.assert_json_equal('', 'socialdeclaration/@1/quarter', 2)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_other', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/id', 3)
        self.assert_json_equal('', 'socialdeclaration/@2/quarter', 3)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_other', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/id', 4)
        self.assert_json_equal('', 'socialdeclaration/@3/quarter', 4)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_other', 0)

        self.factory.xfer = SocialDeclarationCalcul()
        self.calljson('/diacamma.microbusiness/socialDeclarationCalcul', {'socialdeclaration': '1;2;3;4'}, False)
        self.assert_observer('core.dialogbox', 'diacamma.microbusiness', 'socialDeclarationCalcul')

        self.factory.xfer = SocialDeclarationCalcul()
        self.calljson('/diacamma.microbusiness/socialDeclarationCalcul', {'socialdeclaration': '1;2;3;4', "CONFIRME": "YES"}, False)
        self.assert_observer('core.acknowledge', 'diacamma.microbusiness', 'socialDeclarationCalcul')

        self.factory.xfer = SocialDeclarationList()
        self.calljson('/diacamma.microbusiness/socialDeclarationList', {}, False)
        self.assert_observer('core.custom', 'diacamma.microbusiness', 'socialDeclarationList')
        self.assert_json_equal('FLOAT', 'year', current_year)
        self.assert_count_equal('socialdeclaration', 4)
        self.assert_json_equal('', 'socialdeclaration/@0/quarter', 1)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_service', 231)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_other', 0)
        self.assert_json_equal('', 'socialdeclaration/@1/quarter', 2)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_other', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/quarter', 3)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_other', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/quarter', 4)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_other', 0)

        self.factory.xfer = ParamSave()
        self.calljson('/CORE/paramSave', {'params': 'microbusiness-sellaccount;microbusiness-serviceaccount', 'microbusiness-sellaccount': '706', 'microbusiness-serviceaccount': '701'}, False)
        self.assert_observer('core.acknowledge', 'CORE', 'paramSave')

        self.factory.xfer = SocialDeclarationCalcul()
        self.calljson('/diacamma.microbusiness/socialDeclarationCalcul', {'socialdeclaration': '1;2;3;4', "CONFIRME": "YES"}, False)
        self.assert_observer('core.acknowledge', 'diacamma.microbusiness', 'socialDeclarationCalcul')

        self.factory.xfer = SocialDeclarationList()
        self.calljson('/diacamma.microbusiness/socialDeclarationList', {}, False)
        self.assert_observer('core.custom', 'diacamma.microbusiness', 'socialDeclarationList')
        self.assert_json_equal('FLOAT', 'year', current_year)
        self.assert_count_equal('socialdeclaration', 4)
        self.assert_json_equal('', 'socialdeclaration/@0/quarter', 1)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@0/amount_other', 231)
        self.assert_json_equal('', 'socialdeclaration/@1/quarter', 2)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@1/amount_other', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/quarter', 3)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@2/amount_other', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/quarter', 4)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_service', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_sell', 0)
        self.assert_json_equal('', 'socialdeclaration/@3/amount_other', 0)
