# -*- coding: utf-8 -*-
'''
diacamma.pro views package

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
from datetime import date

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from lucterios.framework.tools import MenuManage, FORMTYPE_NOMODAL, CLOSE_NO, FORMTYPE_REFRESH, \
    ActionsManage, SELECT_SINGLE, SELECT_MULTI, FORMTYPE_MODAL, WrapAction
from lucterios.framework.xferadvance import XferListEditor, XferShowEditor, TITLE_EDIT, TITLE_MODIFY
from lucterios.framework.xfercomponents import XferCompFloat, XferCompButton
from lucterios.framework.xfergraphic import XferContainerAcknowledge
from lucterios.CORE.parameters import Params
from lucterios.CORE.views import ParamEdit

from diacamma.microbusiness.models import SocialDeclaration
from diacamma.accounting.models import FiscalYear


MenuManage.add_sub("microbusiness", None, short_icon='mdi:mdi-desktop-classic', caption=_("Microbusiness"), desc=_("Microbusiness tools"), pos=30)


def fill_params(self):
    param_lists = ['microbusiness-simple-socialdeclaration']
    if Params.getvalue('microbusiness-simple-socialdeclaration'):
        param_lists.insert(0, 'microbusiness-serviceaccount')
        param_lists.insert(0, 'microbusiness-sellaccount')
    Params.fill(self, param_lists, 1, self.get_max_row() + 1, nb_col=2)
    btn = XferCompButton('editparam')
    btn.set_location(1, self.get_max_row() + 1, 2, 1)
    btn.set_action(self.request, ParamEdit.get_action(TITLE_MODIFY, short_icon='mdi:mdi-pencil-outline'), close=CLOSE_NO, params={'params': param_lists})
    self.add_component(btn)


@MenuManage.describ('CORE.change_parameter', FORMTYPE_MODAL, 'financial.conf', _('Management of business parameters'))
class BussinessConf(XferListEditor):
    short_icon = 'mdi:mdi-tune'
    caption = _("Microbusiness configuration")

    def fillresponse(self):
        fill_params(self)


def right_socialdeclaration(request):
    if WrapAction('', short_icon='mdi:mdi-desktop-classic', is_view_right='microbusiness.change_socialdeclaration').check_permission(request):
        return Params.getvalue('microbusiness-simple-socialdeclaration')
    else:
        return False


@MenuManage.describ(right_socialdeclaration, FORMTYPE_NOMODAL, 'microbusiness', _('Management of social declarations'))
class SocialDeclarationList(XferListEditor):
    short_icon = 'mdi:mdi-desktop-classic'
    model = SocialDeclaration
    field_id = 'socialdeclaration'
    caption = _("Social declarations")

    def fillresponse_header(self):
        select_year = self.getparam('year', timezone.now().year)
        comp_year = XferCompFloat('year', minval=1900, maxval=2100, precval=0)
        comp_year.set_value(select_year)
        comp_year.set_location(1, 1)
        comp_year.set_action(self.request, self.return_action(), close=CLOSE_NO, modal=FORMTYPE_REFRESH)
        comp_year.description = _('year')
        self.add_component(comp_year)
        self.filter = Q(year=select_year)

        if (FiscalYear.get_current(date(select_year, 1, 1)) is not None) or (FiscalYear.get_current(date(select_year, 12, 31)) is not None):
            for quarter in range(1, 5):
                SocialDeclaration.objects.get_or_create(year=select_year, quarter=quarter)


@ActionsManage.affect_grid(TITLE_EDIT, short_icon='mdi:mdi-text-box-outline', unique=SELECT_SINGLE)
@MenuManage.describ('microbusiness.change_socialdeclaration')
class SocialDeclarationShow(XferShowEditor):
    short_icon = 'mdi:mdi-desktop-classic'
    model = SocialDeclaration
    field_id = 'socialdeclaration'
    caption = _("Show social declarations")


@ActionsManage.affect_grid(_("Calcul"), short_icon='mdi:mdi-pencil-outline', close=CLOSE_NO, unique=SELECT_MULTI)
@ActionsManage.affect_show(_("Calcul"), short_icon='mdi:mdi-pencil-outline', close=CLOSE_NO)
@MenuManage.describ('microbusiness.change_socialdeclaration')
class SocialDeclarationCalcul(XferContainerAcknowledge):
    caption = _("Calcul social declarations")
    short_icon = 'mdi:mdi-desktop-classic'
    model = SocialDeclaration
    field_id = 'socialdeclaration'

    def fillresponse(self):
        if self.confirme(_('Calcul this social declaration ?')):
            for item in self.items:
                item.calcul()
