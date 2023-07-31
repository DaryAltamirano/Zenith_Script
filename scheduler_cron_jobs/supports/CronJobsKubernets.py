from kubernetes import client, config
from kubernetes.client import V1Container, V1PodSpec, V1ObjectMeta, V1PodTemplateSpec, V1JobTemplateSpec, V1CronJob


class CronJobsKubernets:

    def __init__(self):
        # config.load_incluster_config()
        config.load_kube_config()
        self.v1 = client.BatchV1Api()

    def deleteCronJob(self, name, namespace):
        try:
            api_response = self.v1.delete_namespaced_cron_job(name=name, namespace=namespace)
            print("Cronjob eliminado exitosamente.")
        except client.rest.ApiException as e:
            print("Error al eliminar el cronjob:", e)

    def create_cronjob(self, name, namespace):
        config.load_kube_config()

        cron_job = V1CronJob(
            api_version="batch/v1",
            kind="CronJob",
            metadata=V1ObjectMeta(name=name, namespace=namespace),
            spec=V1JobTemplateSpec(

                spec=V1PodTemplateSpec(

                    spec=V1PodSpec(
                        restart_policy="OnFailure",
                        containers=[
                            V1Container(
                                name="test-cronjob-container",
                                image="busybox",
                                command=["echo", "Este es un CronJob de prueba."],
                            )

                        ],
                    )
                )
            ),
        )

        # Crea el CronJob
        try:
            self.v1.create_namespaced_cron_job(body=cron_job, namespace=namespace)
            print(f"CronJob '{name}' creado correctamente.")
        except client.rest.ApiException as e:
            print(f"Error al crear el CronJob '{name}': {e}")