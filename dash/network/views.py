import datetime, requests, json, string, random, pprint

from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0 import client
from novaclient import client as client_nova


from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_principal import Identity, AnonymousIdentity, \
        identity_changed
    
from . import network
from .. import db
from ..models import User, Role, Provider
from ..email import send_email
from ..decorators import requires_roles

def print_values(val, type):
    if type == 'ports':
        val_list = val['ports']
    if type == 'networks':
        val_list = val['networks']
    if type == 'routers':
        val_list = val['routers']
    for p in val_list:
        for k, v in p.items():
            print("%s : %s" % (k, v))
        print('\n')


@network.route('/', methods=['GET', 'POST'])
@login_required
@requires_roles("user","admin")
def index():
    return render_template('network/index.html')
    
@network.route('/list-ips', methods=['GET', 'POST'])
@login_required
@requires_roles("user","admin")
def list_ips():
    user = User.query.get_or_404(current_user.id)
    provider = Provider.query.get_or_404("1")
    auth = identity.Password(auth_url=provider.url,
                             username=user.username,
                             password=user.provider_password,
                             project_name=user.username,
                             project_domain_name='Default',
                             user_domain_name='Default')
    sess = session.Session(auth=auth)
    neutron = client.Client(session=sess)
    nova = client_nova.Client('2', session=sess)
    networks = neutron.list_networks()
    subnets = neutron.list_subnets()
    routers = neutron.list_routers()
    floatingips = neutron.list_floatingips()
    ports = neutron.list_ports()
    return render_template('network/list_ips.html',
                           title="List Networks",
                           block_description = "manage all of your networks",
                           user=user, provider=provider,neutron=neutron,nova=nova,
                           networks=networks,subnets=subnets,routers=routers,
                           floatingips=floatingips, ports=ports,
                           sess=sess)
                           
@network.route('/edit-subnet/<id>', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def edit_subnet(id):
    user = User.query.get_or_404(current_user.id)
    provider = Provider.query.get_or_404("1")
    auth = identity.Password(auth_url=provider.url,
                             username=user.username,
                             password=user.provider_password,
                             project_name=user.username,
                             project_domain_name='Default',
                             user_domain_name='Default')
    sess = session.Session(auth=auth)
    neutron = client.Client(session=sess)
    nova = client_nova.Client('2', session=sess)
    subnet = neutron.list_subnets(id=id)
    ports = neutron.list_ports(subnet_id=id)
    return render_template('network/edit_subnet.html',
                           title="Edit Subnet",
                           block_description = "edit and look subnet details",
                           subnet=subnet,neutron=neutron,ports=ports,nova=nova,
                           sess=sess)