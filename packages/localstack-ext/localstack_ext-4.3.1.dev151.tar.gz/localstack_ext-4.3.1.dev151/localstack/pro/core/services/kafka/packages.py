_E='3.7.x.kraft'
_D='2.8.2.tiered'
_C='3.6.0.1'
_B='2.4.1.1'
_A='3.6.0'
import logging,os
from typing import List,Optional
from localstack.packages import Package,PackageInstaller
from localstack.packages.core import ArchiveDownloadAndExtractInstaller
from localstack.packages.java import JavaInstallerMixin
LOG=logging.getLogger(__name__)
KAFKA_SERVER_URL='https://archive.apache.org/dist/kafka/<version>/kafka_<scala_version>-<version>.tgz'
DEFAULT_VERSION=os.getenv('MSK_DEFAULT_KAFKA_VERSION','').strip()or'3.5.1'
DEPRECATED_MSK_VERSIONS={'1.1.1','2.1.0','2.2.1','2.3.1','2.4.1',_B,'2.5.1',_C}
ACTIVE_MSK_VERSIONS={'2.6.0','2.6.1','2.6.2','2.6.3','2.7.0','2.7.1','2.7.2','2.8.0','2.8.1',_D,'3.1.1','3.2.0','3.3.1','3.3.2','3.4.0','3.5.1',_A,'3.7.x',_E}
KAFKA_VERSION_MAPPING={_D:'2.8.2','3.7.x':'3.7.2',_E:'3.7.2',_B:'2.4.1',_C:_A,'3.6.1':_A}
MSK_VERSIONS=ACTIVE_MSK_VERSIONS|DEPRECATED_MSK_VERSIONS
KAFKA_VERSIONS=MSK_VERSIONS-set(KAFKA_VERSION_MAPPING.keys())|set(KAFKA_VERSION_MAPPING.values())
class KafkaPackage(Package):
	def __init__(A):super().__init__(name='Kafka',default_version=DEFAULT_VERSION)
	def get_versions(A):return list(KAFKA_VERSIONS)
	def _get_installer(A,version):return KafkaPackageInstaller('kafka',version)
class KafkaPackageInstaller(JavaInstallerMixin,ArchiveDownloadAndExtractInstaller):
	@property
	def scala_version(self):
		if self.version>='2.6.0':return'2.13'
		elif self.version>'1.1.1':return'2.12'
		else:return'2.11'
	def _get_download_url(A):return KAFKA_SERVER_URL.replace('<version>',A.version).replace('<scala_version>',A.scala_version)
	def _get_archive_subdir(A):return f"kafka_{A.scala_version}-{A.version}"
	def _get_install_marker_path(A,install_dir):return os.path.join(install_dir,f"kafka_{A.scala_version}-{A.version}",'bin')
kafka_package=KafkaPackage()