"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).
"""

import logging
import yaml
from sonsmbase.smbase import sonSMbase

STATUS_TOPIC= 'specific.manager.registry.ssm.status'
CONFIGURATION_TOPIC = 'son.configuration'

class vEPC_fsm(sonSMbase):

    def __init__(self):

        """
        # FSM/SSM name consists of son,smtype(either ssm or fsm),sfname, name (a-z), and an id (0-9)

        :param smtype: specific management type: either fsm or ssm
        :param sfname: the name of service or function that ssm/fsm belongs to
        :param name: the name of FSM/SSM
        :param id: the Id of FSM/SSM, is used to distinguish between multiple SSM/FSM that are created for the same service
        :param version: version
        :param description: a description on what does FSM/SSM do
        :param uuid: SSM/FSM uuid
        :param sfuuid: service/function uuid that the ssm/fsm belongs to
        """

        self.smtype = 'fsm'
        self.sfname = 'function'
        self.name = 'vEPC'
        self.id = '1'
        self.version = 'v0.1'
        self.description = 'An FSM that reconfigures a VNF'

        self.logger = logging.getLogger("%s.%s" % (self.__module__, self.__class__.__name__))

        super(self.__class__, self).__init__(smtype= self.smtype,
                                             sfname= self.sfname,
                                             name = self.name,
                                             id = self.id,
                                             version = self.version,
                                             description = self.description)

    def _publish(self, topic, **kwords):
        self.manoconn.publish(topic=topic, message=yaml.dump(kwords))

    def on_registration_ok(self):
        self.logger.debug("Received registration ok event.")
        self._publish(STATUS_TOPIC, name=self.name,
                      status="Registration is done, initialising the configuration...")
        self.manoconn.subscribe(self.on_configuration, CONFIGURATION_TOPIC)

    def on_configuration(self, ch, method, props, response):
        self.logger.info('Start configuration ...')
        instantiation_descriptor = yaml.load(str(response))
        vnf_instances = instantiation_descriptor['VNFR']
        host_ip = None
        for vnf in vnf_instances:
            for vdu in vnf['virtual_deployment_units']:
                if vdu['vm_image'] == 'sonata-vfw':
                    host_ip = vdu['vnfc_instance'][0]['connection_points'][0]['type']['address']

        self._publish(STATUS_TOPIC, name=self.name, status="IP address:'%s'" % host_ip)
        self.logger.debug("IP address:'%s'" % host_ip)


def main():
    vEPC_fsm()


if __name__ == '__main__':
    main()
