#!/usr/bin/env python3
import kreate

def kreate_demo_app():
    app = kreate.App('demo', kustomize=True)

    kreate.Ingress(app)
    app.ingress_root.sticky()
    app.ingress_root.whitelist("ggg")
    app.ingress_root.basic_auth()
    app.ingress_root.add_label("dummy", "jan")
    kreate.Ingress(app, path="/api", name="api")

    kreate.Deployment(app)
    #app.depl.add_template_label("egress-to-oracle", "enabled")
    kreate.HttpProbesPatch(app.depl)
    kreate.AntiAffinityPatch(app.depl)
    kreate.Service(app)
    app.service.headless()

    kreate.PodDisruptionBudget(app, name="demo-pdb")
    app.pdb.yaml.spec.minAvailable = 2
    app.pdb.add_label("testje","test")

    kreate.ConfigMap(app, name="demo-vars")
    app.cm.add_var("ENV", value=app.config["env"])
    app.cm.add_var("ORACLE_URL")
    app.cm.add_var("ORACLE_USR")
    app.cm.add_var("ORACLE_SCHEMA")

    return app

kreate.run_cli(kreate_demo_app)