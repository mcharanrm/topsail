import sys

from toolbox._common import RunAnsibleRole, AnsibleRole


ODS_CATALOG_IMAGE_DEFAULT = "quay.io/modh/qe-catalog-source"
ODS_CATALOG_IMAGE_VERSION_DEFAULT = "v160-8"
class RHODS:
    """
    Commands relating to RHODS
    """

    @AnsibleRole("rhods_deploy_ods")
    def deploy_ods(self,
                   catalog_image=ODS_CATALOG_IMAGE_DEFAULT,
                   version=ODS_CATALOG_IMAGE_VERSION_DEFAULT):
        """
        Deploy ODS operator from its custom catalog

        Args:
          catalog_image: Optional. Container image containing ODS bundle.
          version: Optional. Version (catalog image tag) of ODS to deploy.
        """

        opts = {
            "rhods_deploy_ods_catalog_image": catalog_image,
            "rhods_deploy_ods_catalog_image_tag": version,
        }

        return RunAnsibleRole(opts)

    @AnsibleRole("rhods_wait_ods")
    def wait_ods(self):
        """
        Wait for ODS to finish its deployment
        """

        return RunAnsibleRole()

    @AnsibleRole("ocm_deploy_addon")
    def deploy_addon(self,
                     cluster_name, notification_email, wait_for_ready_state=True):
        """
        Installs the RHODS OCM addon

        Args:
          cluster_name: The name of the cluster where RHODS should be deployed.
          notification_email: The email to register for RHODS addon deployment.
          wait_for_ready_state: Optional. If true (default), will cause the role to wait until addon reports ready state. (Can time out)
        """

        addon_parameters = '[{"id":"notification-email","value":"'+notification_email+'"}]'

        opt = {
            "ocm_deploy_addon_id": "managed-odh",
            "ocm_deploy_addon_cluster_name": cluster_name,
            "ocm_deploy_addon_wait_for_ready_state": wait_for_ready_state,
            "ocm_deploy_addon_parameters": addon_parameters,
        }

        return RunAnsibleRole(opt)

    @AnsibleRole("rhods_notebook_ux_e2e_scale_test")
    def notebook_ux_e2e_scale_test(self,
                                   namespace,
                                   idp_name, username_prefix, user_count: int,
                                   secret_properties_file,
                                   notebook_url,
                                   user_index_offset: int = 0,
                                   sut_cluster_kubeconfig="",
                                   artifacts_collected="all",
                                   user_sleep_factor=1.0,
                                   ods_ci_istag="",
                                   ods_ci_exclude_tags="None",
                                   ods_ci_test_case="notebook_ux_e2e_test.robot",
                                   artifacts_exporter_istag="",
                                   notebook_image_name="s2i-generic-data-science-notebook",
                                   notebook_size_name="Small",
                                   notebook_benchmark_name="pyperf_bm_go.py",
                                   notebook_benchmark_number=20,
                                   notebook_benchmark_repeat=2,
                                   state_signal_redis_server="",
                                   toleration_key="",
                                   ):

        """
        End-to-end testing of RHODS notebook user experience at scale

        Args:
          namespace: Namespace in which the scale test should be deployed.
          idp_name: Name of the identity provider to use.
          username_prefix: Prefix of the usernames to use to run the scale test.
          user_count: Number of users to run in parallel.
          user_index_offset: Offset to add to the user index to compute the user name.
          secret_properties_file: Path of a file containing the properties of LDAP secrets. (See 'deploy_ldap' command)
          notebook_url: URL from which the notebook will be downloaded.
          sut_cluster_kubeconfig: Path of the system-under-test cluster's Kubeconfig. If provided, the RHODS endpoints will be looked up in this cluster.
          artifacts_collected:
           - 'all': collect all the artifacts generated by ODS-CI.
           - 'no-screenshot': exclude the screenshots (selenium-screenshot-*.png) from the artifacts collected.
           - 'no-screenshot-except-zero': exclude the screenshots, except if the job index is zero.
           - 'no-screenshot-except-failed': exclude the screenshots, except if the test failed.
           - 'no-screenshot-except-failed-and-zero': exclude the screenshots, except if the test failed or the job index is zero.
           - 'none': do not collect any ODS-CI artifact.
          user_sleep_factor: Delay to sleep between users
          ods_ci_istag: Imagestream tag of the ODS-CI container image.
          ods_ci_scale_test_case: ODS-CI test case to execute.
          ods_ci_exclude_tags: Tags to exclude in the ODS-CI test case.
          artifacts_exporter_istag: Imagestream tag of the artifacts exporter side-car container image.
          ods_ci_notebook_image_name: Name of the RHODS image to use when launching the notebooks.
          ods_ci_notebook_size_name: Name of the RHODS notebook size to select when launching the notebook.
          ods_ci_notebook_benchmark_name: Name of the benchmark to execute in the notebook.
          ods_ci_notebook_benchmark_repeat: Number of repeats of the benchmark to perform.
          ods_ci_notebook_benchmark_number: Number of times the benchmark should be executed within one repeat.
          state_signal_redis_server: Optional. Hostname and port of the Redis server for StateSignal synchronization (for the synchronization of the beginning of the user simulation)
          toleration_key: Optional. Toleration key to use for the test Pods.
        """

        opts = {
            "rhods_notebook_ux_e2e_scale_test_idp_name": idp_name,
            "rhods_notebook_ux_e2e_scale_test_username_prefix": username_prefix,
            "rhods_notebook_ux_e2e_scale_test_user_count": user_count,
            "rhods_notebook_ux_e2e_scale_test_user_index_offset": user_index_offset,
            "rhods_notebook_ux_e2e_scale_test_secret_properties": secret_properties_file,
            "rhods_notebook_ux_e2e_scale_test_notebook_url": notebook_url,
            "rhods_notebook_ux_e2e_scale_test_sut_cluster_kubeconfig": sut_cluster_kubeconfig,
            "rhods_notebook_ux_e2e_scale_test_artifacts_collected": artifacts_collected,
            "rhods_notebook_ux_e2e_scale_test_ods_sleep_factor": ods_sleep_factor,
            "rhods_notebook_ux_e2e_scale_test_ods_ci_test_case": ods_ci_test_case,
            "rhods_notebook_ux_e2e_scale_test_ods_ci_exclude_tags": ods_ci_exclude_tags,
            "rhods_notebook_ux_e2e_scale_test_ods_ci_artifacts_exporter_istag": ods_ci_artifacts_exporter_istag,
            "rhods_notebook_ux_e2e_scale_test_ods_ci_notebook_image_name": ods_ci_notebook_image_name,
            "rhods_notebook_ux_e2e_scale_test_ods_ci_notebook_size_name": ods_ci_notebook_size_name,
            "rhods_notebook_ux_e2e_scale_test_ods_ci_notebook_benchmark_name": ods_ci_notebook_benchmark_name,
            "rhods_notebook_ux_e2e_scale_test_ods_ci_notebook_benchmark_number": ods_ci_notebook_benchmark_number,
            "rhods_notebook_ux_e2e_scale_test_ods_ci_notebook_benchmark_repeat": ods_ci_notebook_benchmark_repeat,
            "rhods_notebook_ux_e2e_scale_test_state_signal_redis_server": state_signal_redis_server,
            "rhods_notebook_ux_e2e_scale_test_toleration_key": toleration_key,
        }

        ARTIFACTS_COLLECTED_VALUES = ("all", "none", "no-screenshot", "no-screenshot-except-zero", "no-screenshot-except-failed", "no-screenshot-except-failed-and-zero")
        if artifacts_collected not in ARTIFACTS_COLLECTED_VALUES:
            print(f"ERROR: invalid value '{artifacts_collected}' for 'artifacts_collected'. Must be one of {', '.join(ARTIFACTS_COLLECTED_VALUES)}")
            sys.exit(1)


        return RunAnsibleRole(opts)

    @AnsibleRole("rhods_cleanup_notebooks")
    def cleanup_notebooks(self,
                          username_prefix):
        """
        Clean up the resources created along with the notebooks, during the scale tests.

        Args:
          username_prefix: Prefix of the usernames who created the resources.
        """

        opts = {
            "rhods_cleanup_notebooks_username_prefix": username_prefix,
        }

        return RunAnsibleRole(opts)

    @AnsibleRole("rhods_notebook_api_scale_test")
    def notebook_api_scale_test(self,
                                namespace,
                                idp_name,
                                secret_properties_file,
                                username_prefix,
                                test_name,
                                user_count: int,
                                run_time="1m",
                                spawn_rate="1",
                                sut_cluster_kubeconfig="",
                                notebook_image_name="s2i-generic-data-science-notebook",
                                api_scale_test_istag="ods-ci:api-scale-test",
                                artifacts_exporter_istag="ods-ci:artifacts-exporter",
                                toleration_key="",
                                ):

        """
        End-to-end testing of RHODS notebook user experience at scale

        Args:
          namespace: Namespace where the test will run
          idp_name: Name of the identity provider to use.
          secret_properties_file: Path of a file containing the properties of LDAP secrets. (See 'deploy_ldap' command).
          username_prefix: Prefix of the RHODS users.
          test_name: Test to perform.
          user_count: Number of users to run in parallel.
          notebook_image_name: Optional. Name of the RHODS image to use when launching the notebooks.

          run_time: Test run time (eg, 300s, 20m, 3h, 1h30m, etc.)
          spawn_rate: Rate to spawn users at (users per second)
          sut_cluster_kubeconfig: Optional. Path of the system-under-test cluster's Kubeconfig. If provided, the RHODS endpoints will be looked up in this cluster.
          toleration_key: Optional. Toleration key to use for the test Pods.
          artifacts_exporter_istag: Optional. Imagestream tag of the artifacts exporter side-car container.
        """

        opts = {
            "rhods_notebook_api_scale_test_namespace": namespace,
            "rhods_notebook_api_scale_test_idp_name": idp_name,
            "rhods_notebook_api_scale_test_secret_properties": secret_properties_file,
            "rhods_notebook_api_scale_test_username_prefix": username_prefix,
            "rhods_notebook_api_scale_test_user_count": user_count,
            "rhods_notebook_api_scale_test_test_name": test_name,
            "rhods_notebook_api_scale_test_run_time": run_time,
            "rhods_notebook_api_scale_test_spawn_rate": spawn_rate,
            "rhods_notebook_api_scale_test_sut_cluster_kubeconfig": sut_cluster_kubeconfig,
            "rhods_notebook_api_scale_test_ods_ci_notebook_image_name": notebook_image_name,
            "rhods_notebook_api_scale_test_toleration_key": toleration_key,
            "rhods_notebook_api_scale_test_artifacts_exporter_istag": artifacts_exporter_istag,
            "rhods_notebook_api_scale_test_istag": api_scale_test_istag,
        }

        return RunAnsibleRole(opts)

    @AnsibleRole("rhods_undeploy_ods")
    def undeploy_ods(self,
                     namespace="redhat-ods-operator",
                     wait: bool = True):
        """
        Undeploy ODS operator

        args:
          wait: Optional. Wait for the operator full deletion.
        """

        opts = {
            "rhods_undeploy_ods_wait": wait,
        }

        return RunAnsibleRole(opts)

    @AnsibleRole("rhods_cleanup_aws")
    def cleanup_aws(self):
        """
        Cleanup AWS from RHODS dangling resources
        """

        return RunAnsibleRole(self)

    @AnsibleRole("cluster_prometheus_db")
    def reset_prometheus_db(self):
        """
        Resets RHODS Prometheus database, by destroying its Pod.
        """

        opts = {
            "cluster_prometheus_db_mode": "reset",
            "cluster_prometheus_db_label": "deployment=prometheus",
            "cluster_prometheus_db_namespace": "redhat-ods-monitoring",
        }

        return RunAnsibleRole(opts)

    @AnsibleRole("cluster_prometheus_db")
    def dump_prometheus_db(self,
                           name_prefix="prometheus"):
        """
        Dump Prometheus database into a file

        Args:
          name_prefix: Optional. Name prefix for the archive that will be stored.
        """

        opts = {
            "cluster_prometheus_db_mode": "dump",
            "cluster_prometheus_db_label": "deployment=prometheus",
            "cluster_prometheus_db_namespace": "redhat-ods-monitoring",
            "cluster_prometheus_db_directory": "/prometheus/data",
            "cluster_prometheus_db_dump_name_prefix": name_prefix,
        }

        return RunAnsibleRole(opts)

    @AnsibleRole("rhods_capture_state")
    def capture_state(self):
        """
        Capture information about the cluster and the RHODS deployment
        """

        return RunAnsibleRole()
