from kubernetes import client, config


class ConnectionRabbitMQ:

    def __init__(self):
        config.load_incluster_config()
        self.v1 = client.BatchV1beta1Api()

    def deleteCronJob(self, name):
        try:
            api_response = self.v1.delete_namespaced_cron_job(name=name, namespace="zenith")
            print("Cronjob eliminado exitosamente.")
        except client.rest.ApiException as e:
            print("Error al eliminar el cronjob:", e)

    def create_cronjob(self, name):
        # Carga la configuración de Kubernetes desde el archivo kubeconfig (si está presente)
        config.load_kube_config()

        # Crea un objeto de configuración del cronjob
        cronjob = client.V1beta1CronJob(api_version="batch/v1beta1", kind="CronJob")
        cronjob.metadata = client.V1ObjectMeta(name=name)

        # Define la especificación del cronjob
        cronjob.spec = client.V1beta1CronJobSpec(
            schedule="*/1 * * * *",  # Cron schedule (every minute)
            job_template=client.V1beta1JobTemplateSpec(
                spec=client.V1JobSpec(
                    template=client.V1PodTemplateSpec(
                        spec=client.V1PodSpec(
                            containers=[
                                client.V1Container(
                                    name="my-container",
                                    image="my-image",
                                    command=["python", "my_script.py"],  # Command to run in the container
                                )
                            ],
                            restart_policy="OnFailure"  # Restart policy for the container
                        )
                    )
                )
            )
        )

        # Crea el objeto cronjob en Kubernetes
        api_instance = client.BatchV1beta1Api()
        api_instance.create_namespaced_cron_job(namespace="zenith", body=cronjob)

        print("Cronjob creado correctamente.")