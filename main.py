# Initialize Mistral client
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import json

from mistralai import Mistral
from mistralai.models import AssistantMessage, SystemMessage, UserMessage

app = FastAPI()

# Initialize Mistral client
api_key = "WOsXWjeJ6HQjxA2zflN5FlAJs8vw9Iav"
# api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY environment variable not set.")
client = Mistral(api_key=api_key)

DEFAULT_MODEL = "mistral-large-latest"
DEFAULT_TEMPERATURE = 0.7

aws_icons = [
        "aws-athena",
        "aws-cloudsearch",
        "aws-emr",
        "aws-finspace",
        "aws-kinesis",
        "aws-kinesis-data-analytics",
        "aws-kinesis-data-streams",
        "aws-kinesis-firehose",
        "aws-kinesis-video-streams",
        "aws-managed-streaming-for-apache-kafka",
        "aws-opensearch-service",
        "aws-quicksight",
        "aws-redshift",
        "aws-data-exchange",
        "aws-data-pipeline",
        "aws-glue",
        "aws-glue-databrew",
        "aws-glue-elastic-views",
        "aws-lake-formation",
        "aws-api-gateway",
        "aws-appflow",
        "aws-eventbridge",
        "aws-managed-workflows-for-apache-airflow",
        "aws-mq",
        "aws-simple-notification-service",
        "aws-simple-queue-service",
        "aws-appsync",
        "aws-console-mobile-application",
        "aws-express-workflows",
        "aws-step-functions",
        "aws-managed-blockchain",
        "aws-quantum-ledger-database",
        "aws-alexa-for-business",
        "aws-chime",
        "aws-chime-sdk",
        "aws-chime-voice-connector",
        "aws-connect",
        "aws-honeycode",
        "aws-pinpoint",
        "aws-pinpoint-apis",
        "aws-simple-email-service",
        "aws-workdocs",
        "aws-workdocs-sdk",
        "aws-workmail",
        "aws-application-cost-profiler",
        "aws-billing-conductor",
        "aws-budgets",
        "aws-cost-and-usage-report",
        "aws-cost-explorer",
        "aws-reserved-instance-reporting",
        "aws-savings-plans",
        "aws-ec2",
        "aws-ec2-auto-scaling",
        "aws-ec2-image-builder",
        "aws-ec2-m5n",
        "aws-ec2-r5n",
        "aws-elastic-container-kubernetes",
        "aws-elastic-container-registry",
        "aws-elastic-container-service",
        "aws-genomics-cli",
        "aws-lightsail",
        "aws-app-runner",
        "aws-batch",
        "aws-compute-optimizer",
        "aws-elastic-beanstalk",
        "aws-fargate",
        "aws-lambda",
        "aws-local-zones",
        "aws-nitro-enclaves",
        "aws-outposts-family",
        "aws-outposts-rack",
        "aws-outposts-servers",
        "aws-parallelcluster",
        "aws-serverless-application-repository",
        "aws-thinkbox-deadline",
        "aws-thinkbox-frost",
        "aws-thinkbox-krakatoa",
        "aws-thinkbox-sequoia",
        "aws-thinkbox-stoke",
        "aws-thinkbox-xmesh",
        "aws-wavelength",
        "aws-bottlerocket",
        "aws-elastic-fabric-adapter",
        "aws-nice-dcv",
        "aws-nice-enginframe",
        "aws-vmware-cloud-on-aws",
        "aws-ecs-anywhere",
        "aws-eks-anywhere",
        "aws-eks-cloud",
        "aws-eks-distro",
        "aws-elastic-kubernetes-service",
        "aws-red-hat-openshift",
        "aws-activate",
        "aws-iq",
        "aws-managed-services",
        "aws-professional-services",
        "aws-repost",
        "aws-support",
        "aws-training-certification",
        "aws-aurora",
        "aws-documentdb",
        "aws-dynamodb",
        "aws-elasticache",
        "aws-keyspaces",
        "aws-memorydb-for-redis",
        "aws-neptune",
        "aws-rds",
        "aws-rds-on-vmware",
        "aws-timestream",
        "aws-database-migration-service",
        "aws-corretto",
        "aws-cloud-control-api",
        "aws-cloud-development-kit",
        "aws-cloud9",
        "aws-cloudshell",
        "aws-codeartifact",
        "aws-codebuild",
        "aws-codecommit",
        "aws-codedeploy",
        "aws-codepipeline",
        "aws-codestar",
        "aws-command-line-interface",
        "aws-tools-and-sdks",
        "aws-x-ray",
        "aws-appstream",
        "aws-worklink",
        "aws-workspaces",
        "aws-workspaces-web",
        "aws-location-service",
        "aws-amplify",
        "aws-device-farm",
        "aws-gamelift",
        "aws-gamesparks",
        "aws-gamekit",
        "aws-open-3d-engine",
        "aws-marketplace",
        "aws-iot-1-click",
        "aws-iot-analytics",
        "aws-iot-button",
        "aws-iot-core",
        "aws-iot-device-defender",
        "aws-iot-device-management",
        "aws-iot-edukit",
        "aws-iot-events",
        "aws-iot-expresslink",
        "aws-iot-fleetwise",
        "aws-iot-greengrass",
        "aws-iot-roborunner",
        "aws-iot-sitewise",
        "aws-iot-things-graph",
        "aws-iot-twinmaker",
        "aws-freertos",
        "aws-augmented-ai-a2i",
        "aws-codeguru",
        "aws-codewhisperer",
        "aws-comprehend",
        "aws-comprehend-medical",
        "aws-devops-guru",
        "aws-elastic-inference",
        "aws-forecast",
        "aws-fraud-detector",
        "aws-healthlake",
        "aws-kendra",
        "aws-lex",
        "aws-lookout-for-equipment",
        "aws-lookout-for-metrics",
        "aws-lookout-for-vision",
        "aws-monitron",
        "aws-personalize",
        "aws-polly",
        "aws-rekognition",
        "aws-sagemaker",
        "aws-sagemaker-ground-truth",
        "aws-sagemaker-studio-lab",
        "aws-textract",
        "aws-transcribe",
        "aws-translate",
        "aws-apache-mxnet-on-aws",
        "aws-deep-learning-amis",
        "aws-deep-learning-containers",
        "aws-deepcomposer",
        "aws-deeplens",
        "aws-deepracer",
        "aws-neuron",
        "aws-panorama",
        "aws-tensorflow-on-aws",
        "aws-torchserve",
        "aws-cloudwatch",
        "aws-managed-grafana",
        "aws-managed-service-for-prometheus",
        "aws-appconfig",
        "aws-application-auto-scaling",
        "aws-auto-scaling",
        "aws-backint-agent",
        "aws-chatbot",
        "aws-cloudformation",
        "aws-cloudtrail",
        "aws-config",
        "aws-control-tower",
        "aws-distro-for-opentelemetry",
        "aws-fault-injection-simulator",
        "aws-launch-wizard",
        "aws-license-manager",
        "aws-management-console",
        "aws-opsworks",
        "aws-organizations",
        "aws-personal-health-dashboard",
        "aws-proton",
        "aws-resilience-hub",
        "aws-service-catalog",
        "aws-systems-manager",
        "aws-systems-manager-incident-manager",
        "aws-trusted-advisor",
        "aws-well-architected-tool",
        "aws-elastic-transcoder",
        "aws-interactive-video-service",
        "aws-nimble-studio",
        "aws-elemental-appliances-&-software",
        "aws-elemental-conductor",
        "aws-elemental-delta",
        "aws-elemental-link",
        "aws-elemental-live",
        "aws-elemental-mediaconnect",
        "aws-elemental-mediaconvert",
        "aws-elemental-medialive",
        "aws-elemental-mediapackage",
        "aws-elemental-mediastore",
        "aws-elemental-mediatailor",
        "aws-elemental-server",
        "aws-application-discovery-service",
        "aws-application-migration-service",
        "aws-datasync",
        "aws-mainframe-modernization",
        "aws-migration-evaluator",
        "aws-migration-hub",
        "aws-server-migration-service",
        "aws-transfer-family",
        "aws-cloud-directory",
        "aws-cloudfront",
        "aws-route-53",
        "aws-virtual-private-cloud",
        "aws-app-mesh",
        "aws-client-vpn",
        "aws-cloud-map",
        "aws-cloud-wan",
        "aws-direct-connect",
        "aws-global-accelerator",
        "aws-private-5g",
        "aws-privatelink",
        "aws-site-to-site-vpn",
        "aws-transit-gateway",
        "aws-elastic-load-balancing",
        "aws-braket",
        "aws-robomaker",
        "aws-ground-station",
        "aws-cognito",
        "aws-detective",
        "aws-guardduty",
        "aws-inspector",
        "aws-macie",
        "aws-artifact",
        "aws-audit-manager",
        "aws-certificate-manager",
        "aws-cloudhsm",
        "aws-directory-service",
        "aws-firewall-manager",
        "aws-iam-identity-center",
        "aws-identity-and-access-management",
        "aws-key-management-service",
        "aws-network-firewall",
        "aws-resource-access-manager",
        "aws-secrets-manager",
        "aws-security-hub",
        "aws-shield",
        "aws-signer",
        "aws-waf",
        "aws-efs",
        "aws-elastic-block-store",
        "aws-fsx",
        "aws-fsx-for-lustre",
        "aws-fsx-for-netapp-ontap",
        "aws-fsx-for-openzfs",
        "aws-fsx-for-wfs",
        "aws-s3-on-outposts",
        "aws-simple-storage-service",
        "aws-simple-storage-service-glacier",
        "aws-backup",
        "aws-snowball",
        "aws-snowball-edge",
        "aws-snowcone",
        "aws-snowmobile",
        "aws-storage-gateway",
        "aws-cloudendure-disaster-recovery",
        "aws-sumerian",
        "aws-analytics",
        "aws-application-integration",
        "aws-blockchain",
        "aws-business-applications",
        "aws-cloud-financial-management",
        "aws-compute",
        "aws-containers",
        "aws-customer-enablement",
        "aws-database",
        "aws-developer-tools",
        "aws-end-user-computing",
        "aws-front-end-web-mobile",
        "aws-game-tech",
        "aws-internet-of-things",
        "aws-machine-learning",
        "aws-management-governance",
        "aws-media-services",
        "aws-migration-transfer",
        "aws-networking-content-delivery",
        "aws-quantum-technologies",
        "aws-robotics",
        "aws-satellite",
        "aws-security-identity-compliance",
        "aws-serverless",
        "aws-storage",
        "aws-vr-ar",
    ]
gcp_icons =  [
        "gcp-access-context-manager",
        "gcp-administration",
        "gcp-advanced-agent-modeling",
        "gcp-advanced-solutions-lab",
        "gcp-agent-assist",
        "gcp-ai-hub",
        "gcp-ai-platform-unified",
        "gcp-ai-platform",
        "gcp-analytics-hub",
        "gcp-anthos-config-management",
        "gcp-anthos-service-mesh",
        "gcp-anthos",
        "gcp-api-analytics",
        "gcp-api-monetization",
        "gcp-api",
        "gcp-apigee-api-platform",
        "gcp-apigee-sense",
        "gcp-app-engine",
        "gcp-artifact-registry",
        "gcp-asset-inventory",
        "gcp-assured-workloads",
        "gcp-automl-natural-language",
        "gcp-automl-tables",
        "gcp-automl-translation",
        "gcp-automl-video-intelligence",
        "gcp-automl-vision",
        "gcp-automl",
        "gcp-bare-metal-solutions",
        "gcp-batch",
        "gcp-beyondcorp",
        "gcp-bigquery",
        "gcp-bigtable",
        "gcp-billing",
        "gcp-binary-authorization",
        "gcp-catalog",
        "gcp-certificate-authority-service",
        "gcp-certificate-manager",
        "gcp-cloud-api-gateway",
        "gcp-cloud-apis",
        "gcp-cloud-armor",
        "gcp-cloud-asset-inventory",
        "gcp-cloud-audit-logs",
        "gcp-cloud-build",
        "gcp-cloud-cdn",
        "gcp-cloud-code",
        "gcp-cloud-composer",
        "gcp-cloud-data-fusion",
        "gcp-cloud-deploy",
        "gcp-cloud-deployment-manager",
        "gcp-cloud-dns",
        "gcp-cloud-domains",
        "gcp-cloud-ekm",
        "gcp-cloud-endpoints",
        "gcp-cloud-external-ip-addresses",
        "gcp-cloud-firewall-rules",
        "gcp-cloud-for-marketing",
        "gcp-cloud-functions",
        "gcp-cloud-generic",
        "gcp-cloud-gpu",
        "gcp-cloud-healthcare-api",
        "gcp-cloud-healthcare-marketplace",
        "gcp-cloud-hsm",
        "gcp-cloud-ids",
        "gcp-cloud-inference-api",
        "gcp-cloud-interconnect",
        "gcp-cloud-jobs-api",
        "gcp-cloud-load-balancing",
        "gcp-cloud-logging",
        "gcp-cloud-media-edge",
        "gcp-cloud-monitoring",
        "gcp-cloud-nat",
        "gcp-cloud-natural-language-api",
        "gcp-cloud-network",
        "gcp-cloud-ops",
        "gcp-cloud-optimization-ai---fleet-routing-api",
        "gcp-cloud-optimization-ai",
        "gcp-cloud-router",
        "gcp-cloud-routes",
        "gcp-cloud-run-for-anthos",
        "gcp-cloud-run",
        "gcp-cloud-scheduler",
        "gcp-cloud-security-scanner",
        "gcp-cloud-shell",
        "gcp-cloud-spanner",
        "gcp-cloud-sql",
        "gcp-cloud-storage",
        "gcp-cloud-tasks",
        "gcp-cloud-test-lab",
        "gcp-cloud-tpu",
        "gcp-cloud-translation-api",
        "gcp-cloud-vision-api",
        "gcp-cloud-vpn",
        "gcp-compute-engine",
        "gcp-configuration-management",
        "gcp-connectivity-test",
        "gcp-connectors",
        "gcp-contact-center-ai",
        "gcp-container-optimized-os",
        "gcp-container-registry",
        "gcp-data-catalog",
        "gcp-data-labeling",
        "gcp-data-layers",
        "gcp-data-loss-prevention-api",
        "gcp-data-qna",
        "gcp-data-studio",
        "gcp-data-transfer",
        "gcp-database-migration-service",
        "gcp-dataflow",
        "gcp-datalab",
        "gcp-dataplex",
        "gcp-datapol",
        "gcp-dataprep",
        "gcp-dataproc-metastore",
        "gcp-dataproc",
        "gcp-datashare",
        "gcp-datastore",
        "gcp-datastream",
        "gcp-debugger",
        "gcp-developer-portal",
        "gcp-dialogflow-cx",
        "gcp-dialogflow-insights",
        "gcp-dialogflow",
        "gcp-document-ai",
        "gcp-early-access-center",
        "gcp-error-reporting",
        "gcp-eventarc",
        "gcp-filestore",
        "gcp-financial-services-marketplace",
        "gcp-firestore",
        "gcp-fleet-engine",
        "gcp-free-trial",
        "gcp-game-servers",
        "gcp-gce-systems-management",
        "gcp-genomics",
        "gcp-gke-on-prem",
        "gcp-google-cloud-marketplace",
        "gcp-google-kubernetes-engine",
        "gcp-google-maps-platform",
        "gcp-healthcare-nlp-api",
        "gcp-home",
        "gcp-identity-and-access-management",
        "gcp-identity-platform",
        "gcp-identity-aware-proxy",
        "gcp-iot-core",
        "gcp-iot-edge",
        "gcp-key-access-justifications",
        "gcp-key-management-service",
        "gcp-kuberun",
        "gcp-launcher",
        "gcp-local-ssd",
        "gcp-looker",
        "gcp-managed-service-for-microsoft-active-directory",
        "gcp-media-translation-api",
        "gcp-memorystore",
        "gcp-migrate-for-anthos",
        "gcp-migrate-for-compute-engine",
        "gcp-my-cloud",
        "gcp-network-connectivity-center",
        "gcp-network-intelligence-center",
        "gcp-network-security",
        "gcp-network-tiers",
        "gcp-network-topology",
        "gcp-onboarding",
        "gcp-os-configuration-management",
        "gcp-os-inventory-management",
        "gcp-os-patch-management",
        "gcp-partner-interconnect",
        "gcp-partner-portal",
        "gcp-performance-dashboard",
        "gcp-permissions",
        "gcp-persistent-disk",
        "gcp-phishing-protection",
        "gcp-policy-analyzer",
        "gcp-premium-network-tier",
        "gcp-private-connectivity",
        "gcp-private-service-connect",
        "gcp-producer-portal",
        "gcp-profiler",
        "gcp-project",
        "gcp-pubsub",
        "gcp-quantum-engine",
        "gcp-quotas",
        "gcp-real-world-insights",
        "gcp-recommendations-ai",
        "gcp-release-notes",
        "gcp-retail-api",
        "gcp-risk-manager",
        "gcp-runtime-config",
        "gcp-secret-manager",
        "gcp-security-command-center",
        "gcp-security-health-advisor",
        "gcp-security-key-enforcement",
        "gcp-security",
        "gcp-service-discovery",
        "gcp-speech-to-text",
        "gcp-stackdriver",
        "gcp-standard-network-tier",
        "gcp-stream-suite",
        "gcp-support",
        "gcp-tensorflow-enterprise",
        "gcp-text-to-speech",
        "gcp-tools-for-powershell",
        "gcp-trace",
        "gcp-traffic-director",
        "gcp-transfer-appliance",
        "gcp-transfer",
        "gcp-user-preferences",
        "gcp-vertexai",
        "gcp-video-intelligence-api",
        "gcp-virtual-private-cloud",
        "gcp-visual-inspection",
        "gcp-vmware-engine",
        "gcp-web-risk",
        "gcp-web-security-scanner",
        "gcp-workflows",
        "gcp-workload-identity-pool",
    ]
general_icons = [
        "activity",
        "airplay",
        "alert-circle",
        "alert-octagon",
        "alert-triangle",
        "align-center",
        "align-justify",
        "align-left",
        "align-right",
        "anchor",
        "aperture",
        "archive",
        "arrow-down-circle",
        "arrow-down-left",
        "arrow-down-right",
        "arrow-down",
        "arrow-left-circle",
        "arrow-left",
        "arrow-right-circle",
        "arrow-right",
        "arrow-up-circle",
        "arrow-up-left",
        "arrow-up-right",
        "arrow-up",
        "at-sign",
        "award",
        "bar-chart-2",
        "bar-chart",
        "battery-charging",
        "battery",
        "bell-off",
        "bell",
        "bold",
        "book-open",
        "book",
        "bookmark",
        "briefcase",
        "calendar",
        "camera-off",
        "camera",
        "cast",
        "check-circle",
        "check-square",
        "check",
        "chevron-down",
        "chevron-left",
        "chevron-right",
        "chevron-up",
        "chevrons-down",
        "chevrons-left",
        "chevrons-right",
        "chevrons-up",
        "circle",
        "clipboard",
        "clock",
        "cloud-drizzle",
        "cloud-lightning",
        "cloud-off",
        "cloud-rain",
        "cloud-snow",
        "cloud",
        "code",
        "coffee",
        "columns",
        "command",
        "compass",
        "copy",
        "corner-down-left",
        "corner-down-right",
        "corner-left-down",
        "corner-left-up",
        "corner-right-down",
        "corner-right-up",
        "corner-up-left",
        "corner-up-right",
        "cpu",
        "credit-card",
        "crop",
        "crosshair",
        "database",
        "delete",
        "disc",
        "divide-circle",
        "divide-square",
        "divide",
        "dollar-sign",
        "download-cloud",
        "download",
        "dribbble",
        "droplet",
        "edit-2",
        "edit-3",
        "edit",
        "external-link",
        "eye-off",
        "eye",
        "fast-forward",
        "feather",
        "file-minus",
        "file-plus",
        "file-text",
        "file",
        "film",
        "filter",
        "flag",
        "folder-minus",
        "folder-plus",
        "folder",
        "framer",
        "frown",
        "gift",
        "git-branch",
        "git-commit",
        "git-merge",
        "git-pull-request",
        "globe",
        "grid",
        "hard-drive",
        "hash",
        "headphones",
        "heart",
        "help-circle",
        "hexagon",
        "home",
        "image",
        "inbox",
        "info",
        "italic",
        "key",
        "layers",
        "layout",
        "life-buoy",
        "link-2",
        "link",
        "list",
        "loader",
        "lock",
        "log-in",
        "log-out",
        "mail",
        "map-pin",
        "map",
        "maximize-2",
        "maximize",
        "meh",
        "menu",
        "message-circle",
        "message-square",
        "mic-off",
        "mic",
        "minimize-2",
        "minimize",
        "minus-circle",
        "minus-square",
        "minus",
        "monitor",
        "moon",
        "more-horizontal",
        "more-vertical",
        "mouse-pointer",
        "move",
        "music",
        "navigation-2",
        "navigation",
        "octagon",
        "package",
        "paperclip",
        "pause-circle",
        "pause",
        "pen-tool",
        "percent",
        "phone-call",
        "phone-forwarded",
        "phone-incoming",
        "phone-missed",
        "phone-off",
        "phone-outgoing",
        "phone",
        "pie-chart",
        "play-circle",
        "play",
        "plus-circle",
        "plus-square",
        "plus",
        "pocket",
        "power",
        "printer",
        "radio",
        "refresh-ccw",
        "refresh-cw",
        "repeat",
        "rewind",
        "rotate-ccw",
        "rotate-cw",
        "save",
        "scissors",
        "search",
        "send",
        "server",
        "settings",
        "share-2",
        "share",
        "shield-off",
        "shield",
        "shopping-bag",
        "shopping-cart",
        "shuffle",
        "sidebar",
        "skip-back",
        "skip-forward",
        "slash",
        "sliders",
        "smartphone",
        "smile",
        "speaker",
        "star",
        "stop-circle",
        "sun",
        "sunrise",
        "sunset",
        "tablet",
        "tag",
        "target",
        "terminal",
        "thermometer",
        "thumbs-down",
        "thumbs-up",
        "toggle-left",
        "toggle-right",
        "tool",
        "trash-2",
        "trash",
        "trello",
        "trending-down",
        "trending-up",
        "triangle",
        "truck",
        "tv",
        "twitch",
        "twitter",
        "type",
        "umbrella",
        "underline",
        "unlock",
        "upload-cloud",
        "upload",
        "user-check",
        "user-minus",
        "user-plus",
        "user-x",
        "user",
        "users",
        "video-off",
        "video",
        "voicemail",
        "volume-1",
        "volume-2",
        "volume-x",
        "volume",
        "watch",
        "wifi-off",
        "wifi",
        "wind",
        "x-circle",
        "x-octagon",
        "x-square",
        "x",
        "zap-off",
        "zap",
        "zoom-in",
        "zoom-out",
    ]
tech_icons = [
        "adobe",
        "airflow",
        "airplay-audio",
        "airplay-video",
        "algolia",
        "alibaba-cloud",
        "alibaba",
        "alipay",
        "amazon",
        "alexa",
        "api-gateway",
        "aws",
        "cloudwatch",
        "dynamodb",
        "rds",
        "s3",
        "sqs",
        "amp",
        "android",
        "angular",
        "ant",
        "apache",
        "cassandra",
        "cloudstack",
        "cordova",
        "couchdb",
        "druid",
        "echarts",
        "flink",
        "groovy",
        "hadoop",
        "hive",
        "kafka",
        "kylin",
        "maven",
        "pulsar",
        "rocketmq",
        "solr",
        "spark",
        "tomcat",
        "apollo-graphql",
        "apple",
        "apple-pay",
        "apple-podcasts",
        "app-store",
        "arduino",
        "assemblyscript",
        "atlassian",
        "auth0",
        "authy",
        "babel",
        "bitcoin",
        "bluetooth",
        "bootstrap",
        "box",
        "brave",
        "bytedance",
        "chromecast",
        "circleci",
        "clojure",
        "cloudflare",
        "cockroach-labs",
        "codepen",
        "codesandbox",
        "coffeescript",
        "confluence",
        "couchbase",
        "cpanel",
        "css3",
        "cypress",
        "dart",
        "databricks",
        "datadog",
        "dbt",
        "debian",
        "deno",
        "discord",
        "django",
        "docker",
        "dot-net",
        "dropbox",
        "drupal",
        "dynamics-365",
        "eclipse-ide",
        "elastic",
        "elasticsearch",
        "electron",
        "elixir",
        "eslint",
        "ethereum",
        "facebook",
        "fastly",
        "figma",
        "firebase",
        "firefox",
        "flask",
        "flutter",
        "gatsby",
        "git",
        "github",
        "github-actions",
        "gitlab",
        "gmail",
        "gnome",
        "gnu",
        "gnu-bash",
        "gnu-emacs",
        "go",
        "google",
        "google-analytics",
        "google-calendar",
        "chrome",
        "google-cloud",
        "google-drive",
        "google-maps",
        "google-meet",
        "google-sheets",
        "google-tag-manager",
        "grafana",
        "graphql",
        "haskell",
        "hasura",
        "heroku",
        "homebrew",
        "html5",
        "hubspot",
        "ibm",
        "ibm-cloud",
        "ibm-watson",
        "instagram",
        "intellij-idea",
        "intercom",
        "internet-explorer",
        "ios",
        "jamstack",
        "javascript",
        "jekyll",
        "jenkins",
        "jest",
        "jetbrains",
        "jira",
        "jquery",
        "json",
        "jupyter",
        "kibana",
        "kotlin",
        "kubernetes",
        "laravel",
        "linkedin",
        "linux",
        "lodash",
        "looker",
        "loom",
        "magento",
        "mapbox",
        "mariadb",
        "markdown",
        "marketo",
        "messenger",
        "meta",
        "meteor",
        "microsoft",
        "access",
        "azure",
        "bing",
        "edge",
        "excel",
        "exchange",
        "office",
        "outlook",
        "powerpoint",
        "sharepoint",
        "sql-server",
        "teams",
        "word",
        "mongodb",
        "mozilla",
        "mysql",
        "neo4j",
        "netlify",
        "next",
        "nginx",
        "nintendo",
        "node",
        "npm",
        "oculus",
        "okta",
        "oracle",
        "perl",
        "php",
        "playstation",
        "postgres",
        "postman",
        "power-bi",
        "powershell",
        "prisma",
        "pulumi",
        "puppeteer",
        "python",
        "pytorch",
        "rabbitmq",
        "railway",
        "raspberry-pi",
        "react",
        "red-hat",
        "redis",
        "redux",
        "rss",
        "rstudio",
        "ruby-on-rails",
        "rust",
        "safari",
        "salesforce",
        "sap",
        "scala",
        "sentry",
        "shopify",
        "slack",
        "snowflake",
        "splunk",
        "sqlite",
        "square",
        "stripe",
        "svelte",
        "swagger",
        "swift",
        "tableau",
        "tencent-qq",
        "tensorflow",
        "terraform",
        "typescript",
        "ubuntu",
        "unity",
        "vercel",
        "vs-code",
        "vite",
        "vue",
        "webassembly",
        "webflow",
        "webgl",
        "webpack",
        "webrtc",
        "wechat",
        "whatsapp",
        "windows",
        "wordpress",
        "xbox",
        "youtube",
        "zendesk",
        "zoom",
    ]
azure_icons = [
    "azure-batch-ai"
    "azure-machine-learning-studio-classic-web-services"
    "azure-genomics"
    "azure-translator-text"
    "azure-experimentation-studio"
    "azure-object-understanding"
    "azure-cognitive-services"
    "azure-genomics-accounts"
    "azure-bot-services"
    "azure-machine-learning"
    "azure-machine-learning-studio-workspaces"
    "azure-machine-learning-studio-web-service-plans"
    "azure-applied-ai"
    "azure-language-services"
    "azure-log-analytics-workspaces"
    "azure-event-hubs"
    "azure-stream-analytics-jobs"
    "azure-endpoint-analytics"
    "azure-synapse-analytics"
    "azure-workbooks"
    "azure-hd-insight-clusters"
    "azure-data-lake-analytics"
    "azure-analysis-services"
    "azure-event-hub-clusters"
    "azure-data-lake-store-gen1"
    "azure-databricks"
    "azure-app-service-plans"
    "azure-app-service-certificates"
    "azure-app-service-domains"
    "azure-cdn-profiles"
    "azure-app-services"
    "azure-api-management-services"
    "azure-search-services"
    "azure-notification-hubs"
    "azure-app-service-environments"
    "azure-collaborative-service"
    "azure-applens"
    "azure-hybrid-center"
    "azure-multi-tenancy"
    "azure-infrastructure-backup"
    "azure-capacity"
    "azure-offers"
    "azure-user-subscriptions"
    "azure-plans"
    "azure-stack"
    "azure-updates"
    "azure-avs"
    "azure-blockchain-applications"
    "azure-outbound-connection"
    "azure-blockchain-service"
    "azure-token-service"
    "azure-abs-member"
    "azure-consortium"
    "azure-maintenance-configuration"
    "azure-disk-encryption-sets"
    "azure-workspaces"
    "azure-automanaged-vm"
    "azure-managed-service-fabric"
    "azure-metrics-advisor"
    "azure-image-templates"
    "azure-restore-points"
    "azure-restore-points-collections"
    "azure-compute-galleries"
    "azure-virtual-machine"
    "azure-kubernetes-services"
    "azure-mesh-applications"
    "azure-availability-sets"
    "azure-disks-snapshots"
    "azure-os-images-classic"
    "azure-virtual-machines-classic"
    "azure-function-apps"
    "azure-cloud-services-classic"
    "azure-batch-accounts"
    "azure-disks"
    "azure-images"
    "azure-vm-scale-sets"
    "azure-service-fabric-clusters"
    "azure-image-definitions"
    "azure-image-versions"
    "azure-shared-image-galleries"
    "azure-vm-images-classic"
    "azure-disks-classic"
    "azure-container-services-deprecated"
    "azure-container-instances"
    "azure-host-groups"
    "azure-hosts"
    "azure-spring-cloud"
    "azure-container-registries"
    "azure-sql-data-warehouses"
    "azure-sql"
    "azure-ssis-lift-and-shift-ir"
    "azure-purview-accounts"
    "azure-sql-edge"
    "azure-database-postgresql-server-group"
    "azure-cosmos-db"
    "azure-database-mysql-server"
    "azure-database-mariadb-server"
    "azure-sql-vm"
    "azure-data-factory"
    "azure-virtual-clusters"
    "azure-elastic-job-agents"
    "azure-sql-database"
    "azure-database-postgresql-server"
    "azure-sql-server"
    "azure-database-migration-services"
    "azure-sql-elastic-pools"
    "azure-managed-database"
    "azure-sql-managed-instance"
    "azure-sql-server-stretch-databases"
    "azure-cache-redis"
    "azure-instance-pools"
    "azure-data-explorer-clusters"
    "azure-sql-server-registries"
    "azure-application-insights"
    "azure-cloudtest"
    "azure-devops"
    "azure-devtest-labs"
    "azure-lab-services"
    "azure-cost-management-and-billing"
    "azure-preview-features"
    "azure-all-resources"
    "azure-subscriptions"
    "azure-reservations"
    "azure-service-health"
    "azure-information"
    "azure-recent"
    "azure-resource-groups"
    "azure-marketplace"
    "azure-templates"
    "azure-quickstart-center"
    "azure-management-groups"
    "azure-help-and-support"
    "azure-tag"
    "azure-dashboard"
    "azure-free-services"
    "azure-cost-management"
    "azure-region-management"
    "azure-troubleshoot"
    "azure-resource-explorer"
    "azure-biz-talk"
    "azure-blob-block"
    "azure-blob-page"
    "azure-branch"
    "azure-browser"
    "azure-bug"
    "azure-builds"
    "azure-cache"
    "azure-code"
    "azure-commit"
    "azure-controls"
    "azure-controls-horizontal"
    "azure-cost-alerts"
    "azure-cost-analysis"
    "azure-cost-budgets"
    "azure-counter"
    "azure-cubes"
    "azure-dev-console"
    "azure-download"
    "azure-error"
    "azure-extensions"
    "azure-file"
    "azure-files"
    "azure-folder-blank"
    "azure-folder-website"
    "azure-ftp"
    "azure-gear"
    "azure-globe-error"
    "azure-globe-success"
    "azure-globe-warning"
    "azure-guide"
    "azure-heart"
    "azure-image"
    "azure-input-output"
    "azure-journey-hub"
    "azure-launch-portal"
    "azure-learn"
    "azure-load-test"
    "azure-location"
    "azure-log-streaming"
    "azure-management-portal"
    "azure-media-file"
    "azure-mobile"
    "azure-mobile-engagement"
    "azure-power"
    "azure-powershell"
    "azure-power-up"
    "azure-preview"
    "azure-process-explorer"
    "azure-production-ready-database"
    "azure-resource-group-list"
    "azure-resource-linked"
    "azure-scale"
    "azure-scheduler"
    "azure-search"
    "azure-server-farm"
    "azure-ssd"
    "azure-storage-azure-files"
    "azure-storage-container"
    "azure-storage-queue"
    "azure-table"
    "azure-tags"
    "azure-tfs-vc-repository"
    "azure-toolbox"
    "azure-versions"
    "azure-website-power"
    "azure-website-staging"
    "azure-web-slots"
    "azure-web-test"
    "azure-workflow"
    "azure-backlog"
    "azure-media"
    "azure-module"
    "azure-search-grid"
    "azure-verifiable-credentials"
    "azure-pim"
    "azure-tenant-properties"
    "azure-custom-azure-ad-roles"
    "azure-aad-licenses"
    "azure-active-directory"
    "azure-ad-domain-services"
    "azure-groups"
    "azure-active-directory-connect-health"
    "azure-enterprise-applications"
    "azure-managed-identities"
    "azure-ad-b2c"
    "azure-information-protection"
    "azure-users"
    "azure-ad-identity-protection"
    "azure-app-registrations"
    "azure-ad-privilege-identity-management"
    "azure-identity-governance"
    "azure-integration-service-environments"
    "azure-partner-topic"
    "azure-system-topic"
    "azure-partner-registration"
    "azure-partner-namespace"
    "azure-logic-apps"
    "azure-event-grid-topics"
    "azure-relays"
    "azure-api-for-fhir"
    "azure-software-as-a-service"
    "azure-event-grid-domains"
    "azure-data-catalog"
    "azure-integration-accounts"
    "azure-app-configuration"
    "azure-sendgrid-accounts"
    "azure-event-grid-subscriptions"
    "azure-logic-apps-custom-connector"
    "azure-service-bus"
    "azure-time-series-insights-access-policies"
    "azure-device-security-apple"
    "azure-device-security-google"
    "azure-device-security-windows"
    "azure-intune"
    "azure-ebooks"
    "azure-client-apps"
    "azure-devices"
    "azure-device-compliance"
    "azure-software-updates"
    "azure-security-baselines"
    "azure-device-enrollment"
    "azure-device-configuration"
    "azure-exchange-access"
    "azure-ad-roles-and-administrators"
    "azure-tenant-status"
    "azure-intune-for-education"
    "azure-intune-app-protection"
    "azure-mindaro"
    "azure-digital-twins"
    "azure-industrial-iot"
    "azure-time-series-insights-environments"
    "azure-iot-hub"
    "azure-iot-central-applications"
    "azure-maps-accounts"
    "azure-iot-edge"
    "azure-time-series-insights-event-sources"
    "azure-time-series-data-sets"
    "azure-windows10-core-services"
    "azure-device-provisioning-services"
    "azure-monitor"
    "azure-alerts"
    "azure-advisor"
    "azure-blueprints"
    "azure-activity-log"
    "azure-diagnostics-settings"
    "azure-scheduler-job-collections"
    "azure-compliance"
    "azure-my-customers"
    "azure-recovery-services-vaults"
    "azure-metrics"
    "azure-solutions"
    "azure-automation-accounts"
    "azure-operation-log-classic"
    "azure-service-providers"
    "azure-education"
    "azure-service-catalog-mad"
    "azure-lighthouse"
    "azure-universal-print"
    "azure-arc"
    "azure-user-privacy"
    "azure-managed-desktop"
    "azure-managed-applications-center"
    "azure-customer-lockbox-for-microsoft-azure"
    "azure-policy"
    "azure-resource-graph-explorer"
    "azure-machinesazurearc"
    "azure-keys"
    "azure-data-box"
    "azure-data-box-edge"
    "azure-migrate"
    "azure-remote-rendering"
    "azure-spatial-anchor-accounts"
    "azure-sap-azure-monitor"
    "azure-firewall-manager"
    "azure-private-link"
    "azure-ip-groups"
    "azure-private-link-service"
    "azure-resource-management-private-link"
    "azure-private-link-hub"
    "azure-load-balancer-hub"
    "azure-bastions"
    "azure-virtual-router"
    "azure-spot-vmss"
    "azure-spot-vm"
    "azure-dns-private-resolver"
    "azure-virtual-networks"
    "azure-load-balancers"
    "azure-virtual-network-gateways"
    "azure-dns-zones"
    "azure-traffic-manager-profiles"
    "azure-network-watcher"
    "azure-network-security-groups"
    "azure-public-ip-addresses-classic"
    "azure-public-ip-addresses"
    "azure-on-premises-data-gateways"
    "azure-route-filters"
    "azure-ddos-protection-plans"
    "azure-front-doors"
    "azure-virtual-networks-classic"
    "azure-application-gateways"
    "azure-local-network-gateways"
    "azure-expressroute-circuits"
    "azure-network-interfaces"
    "azure-connections"
    "azure-route-tables"
    "azure-firewalls"
    "azure-service-endpoint-policies"
    "azure-nat"
    "azure-virtual-wans"
    "azure-web-application-firewall-policies-waf"
    "azure-proximity-placement-groups"
    "azure-reserved-ip-addresses-classic"
    "azure-public-ip-prefixes"
    "azure-intune-trends"
    "azure-dashboard-hub"
    "azure-avs-vm"
    "azure-network-manager"
    "azure-dedicated-hsm"
    "azure-modular-data-center"
    "azure-api-proxy"
    "azure-fiji"
    "azure-monitor-dashboard"
    "azure-support-center-blue"
    "azure-connected-cache"
    "azure-web-app-+-database"
    "azure-hpc-workbench"
    "azure-connected-vehicle-platform"
    "azure-aquila"
    "azure-reserved-capacity"
    "azure-custom-ip-prefix"
    "azure-confidential-ledger"
    "azure-reserved-capacity-groups"
    "azure-windows-notification-services"
    "azure-mission-landing-zone"
    "azure-private-mobile-network"
    "azure-vm-application-definition"
    "azure-vm-application-version"
    "azure-edge-hardware-center"
    "azure-ceres"
    "azure-azurite"
    "azure-update-center"
    "azure-image-definition"
    "azure-image-version"
    "azure-savings-plan"
    "azure-worker-container-app"
    "azure-grafana"
    "azure-storage-tasks"
    "azure-sonic-dash"
    "azure-compliance-center"
    "azure-load-testing"
    "azure-acs-solutions-builder"
    "azure-container-app-environments"
    "azure-marketplace-management"
    "azure-edge-management"
    "azure-sphere"
    "azure-exchange-on-premises-access"
    "azureattestation"
    "azure-web-jobs"
    "azure-windows-virtual-desktop"
    "azure-ssh-keys"
    "azure-internet-analyzer-profiles"
    "azure-cloud-shell"
    "azure-expressroute-direct"
    "azure-communication-services"
    "azure-peering-service"
    "azure-resource-mover"
    "azure-chaos-studio"
    "azure-template-specs"
    "azure-backup-center"
    "azure-device-update-iot-hub"
    "azure-cloud-services-extended-support"
    "azure-disk-pool"
    "azure-bare-metal-infrastructure"
    "azure-open-supply-chain-platform"
    "azure-managed-instance-apache-cassandra"
    "azure-test-base"
    "azure-orbital"
    "azure-network-function-manager"
    "azure-quotas"
    "azure-wac"
    "azure-rtos"
    "azure-detonation"
    "azure-defender"
    "azure-conditional-access"
    "azure-security-center"
    "azure-application-security-groups"
    "azure-key-vaults"
    "azure-sentinel"
    "azure-extendedsecurityupdates"
    "azure-stack-edge"
    "azure-hcp-cache"
    "azure-storage-accounts"
    "azure-storage-accounts-classic"
    "azure-storsimple-device-managers"
    "azure-data-lake-storage-gen1"
    "azure-storage-explorer"
    "azure-storsimple-data-managers"
    "azure-storage-sync-services"
    "azure-netapp-files"
    "azure-data-share-invitations"
    "azure-data-shares"
    "azure-import-export-jobs"
    "azure-fileshare"
    "azure-static-apps"
    "azure-api-connections"
    "azure-signalr"
    "azure-notification-hub-namespaces"
    "azure-media-service"
]
kubernetes_icons = [
    "k8s-kubernetes"
    "k8s-api"
    "k8s-c-c-m"
    "k8s-c-m"
    "k8s-k-proxy"
    "k8s-kubelet"
    "k8s-sched"
    "k8s-control-plane"
    "k8s-node"
    "k8s-etcd"
    "k8s-c-role"
    "k8s-cm"
    "k8s-crb"
    "k8s-crd"
    "k8s-cronjob"
    "k8s-deploy"
    "k8s-ds"
    "k8s-ep"
    "k8s-group"
    "k8s-hpa"
    "k8s-ing"
    "k8s-job"
    "k8s-limits"
    "k8s-netpol"
    "k8s-ns"
    "k8s-pod"
    "k8s-psp"
    "k8s-pv"
    "k8s-pvc"
    "k8s-quota"
    "k8s-rb"
    "k8s-role"
    "k8s-rs"
    "k8s-sa"
    "k8s-sc"
    "k8s-secret"
    "k8s-sts"
    "k8s-svc"
    "k8s-user"
    "k8s-vol"
]


# Configure CORS
# origins = [
#     "http://localhost:3000", 
#     "http://localhost:8000", 
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,  # Allow credentials (cookies, authorization headers, etc.)
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers
)

class ChatRequest(BaseModel):
    session_id: str
    message: str
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    system_message: Optional[str] = None
    cloud_provider: str = "AWS"

class ChatSession:
    def __init__(self, model, temperature, system_message):
        self.model = model
        self.temperature = temperature
        self.system_message = system_message
        self.messages = []

sessions = {}

@app.post("/new_chat")
def new_chat(model: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE, system_message: Optional[str] = None):
    session_id = str(len(sessions) + 1)
    sessions[session_id] = ChatSession(model, temperature, system_message)
    return {"session_id": session_id}

@app.post("/chat")
def chat(request: ChatRequest):
    session_id = request.session_id
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    chat_session = sessions[session_id]
    
    def prompt_enhancer(problem_statement, cloud_provider):
        try:
            chat_response = client.chat.complete(
                model=chat_session.model,
                messages=[
                    {
                        "role": "user",
                        "content": f"Problem statement: {problem_statement}\n"
                                    f"Generate a detailed list of key cloud architecture components, services, and their interactions in a structured format "
                                    f"including firewalls, caching mechanisms, and other critical infrastructure elements that ensure security, scalability, performance, deployment and CI/CD. "
                                    f"Clearly define the linking and grouping of these components, ensuring that the architecture is standard, scalable, "
                                    f"and aligns with the specified problem statement.\n"
                                    f"Use {cloud_provider} services. Don't add extra text just provide the solutions."
                    }
                ]
            )

            if hasattr(chat_response, 'choices') and len(chat_response.choices) > 0:
                components = chat_response.choices[0].message.content.strip()
                return components
            else:
                print("No choices found in the response.")
                return ""
        except Exception as e:
            print(f"An error occurred with Mistral: {e}")
            return ""

    # Enhance the problem statement and get the response
    enhanced_problem_statement = prompt_enhancer(request.message, request.cloud_provider)

    # Run inference and collect response
    assistant_response = ""
    chat_session.messages.append(UserMessage(content=request.message))
    
    for chunk in client.chat.stream(
        model=chat_session.model,
        temperature=chat_session.temperature,
        messages=chat_session.messages
    ):
        response = chunk.data.choices[0].delta.content
        if response:
            assistant_response += response
    if assistant_response:
        chat_session.messages.append(AssistantMessage(content=assistant_response))
    
    return {"response": assistant_response}

@app.post("/get_json")
def get_json(request: ChatRequest):
    session_id = request.session_id
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    chat_session = sessions[session_id]
    
    def generate_architecture_response_in_json_format_v1(enhanced_prompt, cloud_provider):
        try:
            if cloud_provider == 'aws':
                all_icons = aws_icons + tech_icons + general_icons + kubernetes_icons
            elif cloud_provider == 'gcp':
                all_icons = gcp_icons + tech_icons + general_icons + kubernetes_icons
            elif cloud_provider == 'azure':
                all_icons = azure_icons + tech_icons + general_icons + kubernetes_icons
            else:
                all_icons = aws_icons + gcp_icons + tech_icons + general_icons + azure_icons + kubernetes_icons
            all_icons_str = ", ".join(all_icons)
            
            # Define the prompt to convert architecture components into JSON
            prompt = f"""
            Convert the following architecture components into a structured JSON format. Ensure that the labels used for nodes only include the icon names from the provided list.
            Include essential components such as users, API firewalls, API gateways, frontend, backend, Konga, load balancers, and other critical elements of the architecture.
            Start with the proper flow from User to the end system.
            {enhanced_prompt}

            The format should be:
            {{
                "nodes": [
                    {{
                        "id": "node_id", # This id must be one of the following: {all_icons_str}
                        "label": "Node Label",
                        "description": "Description of this node"
                    }},
                    ...
                ],
                "edges": [
                    {{
                        "id": "edge_name", # Use descriptive edge names
                        "from": "source_node_id",
                        "to": "target_node_id"
                    }},
                    ...
                ],
                "groups": {{
                    "group_name": {{
                        "id": "group_id",
                        "label": "Group Label",
                        "elements": [
                            "node_id_1",
                            "node_id_2"
                        ]
                    }},
                    ...
                }}
            }}
            **Valid Icon Names**: {all_icons_str}
            
            Please ensure that the labels in the JSON output are only from the valid icon names listed.
            """
            
            # Call the Mistral model
            try:
                chat_response = client.chat.complete(
                    model="mistral-large-latest",
                    messages=[{"role": "user", "content": prompt}]
                )
            except Exception as api_error:
                print(f"An error occurred with Mistral: {api_error}")
                # Fallback or error handling
                return {"error": f"API error occurred: {str(api_error)}"}
            
            # Handle the API response
            if hasattr(chat_response, 'choices') and len(chat_response.choices) > 0:
                components = chat_response.choices[0].message.content.strip()
                
                # Remove code block markers if present
                if components.startswith("```") and components.endswith("```"):
                    components = components.strip("```")
                    components = components.split("\n", 1)[1] if "\n" in components else components
                
                try:
                    json_data = json.loads(components)
                    
                    # Ensure nodes and edges exist in the JSON
                    if "nodes" not in json_data or "edges" not in json_data:
                        return {"error": "Missing nodes or edges in the response JSON.", "content": components}
                    
                    # Map node IDs for validation
                    node_ids = {node["id"] for node in json_data["nodes"]}
                    
                    # Validate and correct edges
                    valid_edges = []
                    for edge in json_data["edges"]:
                        from_node = edge["from"]
                        to_node = edge["to"]
                        
                        # Ensure that both 'from' and 'to' nodes are valid
                        if from_node in node_ids and to_node in node_ids:
                            edge["id"] = f"edge_{from_node}_to_{to_node}"
                            valid_edges.append(edge)
                        else:
                            # Handle wildcard nodes or invalid edges
                            if from_node == '*' or to_node == '*':
                                print(f"Wildcard edge ignored: {edge}")
                            else:
                                print(f"Invalid edge ignored: {edge}")
                    
                    json_data["edges"] = valid_edges
                    
                    # Process groups
                    processed_groups = {}
                    if "groups" in json_data:
                        for group_name, group in json_data["groups"].items():
                            processed_groups[group_name] = {
                                "id": group["id"],
                                "label": group_name,
                                "elements": group["elements"]
                            }
                    json_data["group"] = processed_groups
                    
                    return json_data
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    return {"error": "Invalid JSON returned by the model.", "content": components}
            else:
                return {"error": "No valid response from the model."}
        
        except Exception as e:
            print(f"An error occurred in generate_architecture_response_in_json_format_v1: {e}")
            return {"error": str(e)}


    # Enhance the problem statement and get the response
    json_statement = generate_architecture_response_in_json_format_v1(request.message, request.cloud_provider)
    print("json_statement::::;", json_statement,"---------->>>>")
    if "error" in json_statement:
        # Handle errors returned from generate_architecture_response_in_json_format_v1
        raise HTTPException(status_code=500, detail=json_statement["error"])
    else:
        return json_statement

@app.post("/chat_v1")
def chat_v1(model: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE, system_message: Optional[str] = None):
    session_id = str(len(sessions) + 1)
    sessions[session_id] = ChatSession(model, temperature, system_message)
    return {
    "response": "Creating a cloud-based e-commerce platform requires a thoughtful architectural design that balances scalability, performance, security, and user experience. Here’s a detailed architecture for a cloud-based e-commerce platform:\n\n### 1. **Presentation Layer**\n   - **Web Frontend**: A responsive web application built using frameworks like React, Angular, or Vue.js.\n   - **Mobile Application**: Native or cross-platform mobile apps (e.g., iOS, Android) for enhanced user experience.\n   - **Content Delivery Network (CDN)**: Services like AWS CloudFront or Cloudflare to distribute content globally, reducing latency.\n\n### 2. **Application Layer**\n   - **API Gateway**: Manages API requests, handles rate limiting, authentication, and load balancing (e.g., AWS API Gateway, Kong).\n   - **Microservices Architecture**:\n     - **Product Service**: Manages product catalog, inventory, and metadata.\n     - **Order Service**: Handles order placement, tracking, and fulfillment.\n     - **User Service**: Manages user authentication, profiles, and preferences.\n     - **Payment Service**: Processes transactions through payment gateways (e.g., Stripe, PayPal).\n     - **Shipping Service**: Integrates with shipping providers for logistics management.\n     - **Notification Service**: Sends emails, SMS, or push notifications to users.\n     - **Search Service**: Provides fast and relevant search results (e.g., Elasticsearch).\n     - **Recommendation Service**: Offers personalized product recommendations.\n\n### 3. **Data Layer**\n   - **Relational Databases**: Stores structured data such as user profiles, orders, and product details (e.g., PostgreSQL, MySQL).\n   - **NoSQL Databases**: Stores unstructured or semi-structured data like user sessions, shopping carts (e.g., MongoDB, DynamoDB).\n   - **Caching**: Improves performance by storing frequently accessed data (e.g., Redis, Memcached).\n   - **Data Warehouse**: Stores historical data for analytics and reporting (e.g., Amazon Redshift, Google BigQuery).\n\n### 4. **Integration Layer**\n   - **Message Queues**: Facilitates asynchronous communication between microservices (e.g., RabbitMQ, Apache Kafka).\n   - **Event Sourcing**: Captures all state changes as a sequence of events (e.g., Apache Kafka, AWS EventBridge).\n   - **Third-Party Integrations**: APIs for payment gateways, shipping providers, marketing tools, and other external services.\n\n### 5. **Infrastructure Layer**\n   - **Cloud Provider**: Offers scalable and on-demand infrastructure (e.g., AWS, Google Cloud, Microsoft Azure).\n   - **Compute Resources**: Virtual machines or containers to run applications (e.g., EC2, Google Compute Engine, Kubernetes).\n   - **Storage Solutions**: Object storage for static files, backups, etc. (e.g., S3, Google Cloud Storage).\n   - **Networking**: Virtual Private Clouds (VPCs), subnets, security groups, and load balancers for secure and efficient communication.\n\n### 6. **Monitoring and Logging**\n   - **Monitoring**: Tools to track performance, health, and usage metrics (e.g., Prometheus, Grafana, Datadog).\n   - **Logging**: Collects and analyzes logs for troubleshooting and auditing (e.g., ELK Stack, CloudWatch).\n   - **Alerting**: Notifies administrators of critical issues (e.g., PagerDuty, OpsGenie).\n\n### 7. **Security**\n   - **Authentication and Authorization**: Manages user access and permissions (e.g., OAuth, JWT).\n   - **Encryption**: Protects data at rest and in transit (e.g., SSL/TLS, AES).\n   - **Web Application Firewall (WAF)**: Protects against common web exploits (e.g., AWS WAF, Cloudflare).\n   - **Intrusion Detection and Prevention**: Monitors and blocks malicious activities (e.g., AWS Shield).\n\n### 8. **CI/CD Pipeline**\n   - **Continuous Integration and Deployment**: Automates the build, testing, and deployment process (e.g., Jenkins, GitLab CI/CD, CircleCI).\n   - **Infrastructure as Code (IaC)**: Automates the provisioning and management of infrastructure (e.g., Terraform, AWS CloudFormation).\n\n### 9. **Analytics and Reporting**\n   - **Business Intelligence**: Tools for data visualization and reporting (e.g., Tableau, Power BI).\n   - **Real-time Analytics**: Analyzes user behavior and interactions in real-time (e.g., Google Analytics, Mixpanel).\n\n### 10. **Customer Support and CRM**\n   - **Customer Relationship Management (CRM)**: Manages customer interactions and support tickets (e.g., Salesforce, Zendesk).\n   - **Live Chat and Support**: Provides real-time assistance to customers (e.g., Intercom, Zendesk Chat).\n\n### Architecture Diagram\n\n```plaintext\n+----------------------------------------+\n|                  CDN                    |\n+----------------------------------------+\n|                 Web                    |\n|                 Frontend               |\n|                 Mobile App             |\n+----------------------------------------+\n|                 API Gateway            |\n+----------------------------------------+\n|               Microservices            |\n|  +---------------+  +---------------+   |\n|  |  Product      |  |   Order       |   |\n|  |  Service      |  |   Service     |   |\n|  +---------------+  +---------------+   |\n|  +---------------+  +---------------+   |\n|  |  User         |  |   Payment     |   |\n|  |  Service      |  |   Service     |   |\n|  +---------------+  +---------------+   |\n|  +---------------+  +---------------+   |\n|  |  Shipping     |  |   Notification|   |\n|  |  Service      |  |   Service     |   |\n|  +---------------+  +---------------+   |\n|  +---------------+  +---------------+   |\n|  |  Search       |  |   Recommend.  |   |\n|  |  Service      |  |   Service     |   |\n|  +---------------+  +---------------+   |\n+----------------------------------------+\n|               Data Layer               |\n|  +---------------+  +---------------+  |\n|  |  Relational   |  |   NoSQL        |  |\n|  |  Database     |  |   Database    |  |\n|  +---------------+  +---------------+  |\n|  +---------------+  +---------------+  |\n|  |  Caching       |  |   Data Ware.  |  |\n|  |  (Redis)       |  |   house       |  |\n|  +---------------+  +---------------+  |\n+----------------------------------------+\n|               Integration Layer        |\n|  +---------------+  +---------------+  |\n|  |  Message Queue|  |   Event       |  |\n|  |  (RabbitMQ)   |  |   Sourcing    |  |\n|  +---------------+  +---------------+  |\n|  +---------------+                     |\n|  |  Third-Party  |                     |\n|  |  Integrations |                     |\n|  +---------------+                     |\n+----------------------------------------+\n|               Infrastructure Layer     |\n|  +---------------+  +---------------+  |\n|  |  Cloud        |  |   Compute      |  |\n|  |  Provider     |  |   Resources    |  |\n|  +---------------+  +---------------+  |\n|  +---------------+  +---------------+  |\n|  |  Storage      |  |   Networking   |  |\n|  |  Solutions    |  |   (VPCs)       |  |\n|  +---------------+  +---------------+  |\n+----------------------------------------+\n|               Monitoring & Logging     |\n|  +---------------+  +---------------+  |\n|  |  Monitoring   |  |   Logging      |  |\n|  |  (Prometheus) |  |   (ELK Stack) |  |\n|  +---------------+  +---------------+  |\n|  +---------------+                     |\n|  |  Alerting     |                     |\n|  |  (PagerDuty)  |                     |\n|  +---------------+                     |\n+----------------------------------------+\n|               Security Layer          |\n|  +---------------+  +---------------+  |\n|  |  Auth & Authz |  |   Encryption   |  |\n|  |  (OAuth)      |  |   (SSL/TLS)    |  |\n|  +---------------+  +---------------+  |\n|  +---------------+  +---------------+  |\n|  |  WAF          |  |   IDS/IPS      |  |\n|  |  (AWS WAF)    |  |   (AWS Shield) |  |\n|  +---------------+  +---------------+  |\n+----------------------------------------+\n|               CI/CD Pipeline           |\n|  +---------------+  +---------------+  |\n|  |  CI/CD        |  |   IaC          |  |\n|  |  (Jenkins)    |  |   (Terraform)  |  |\n|  +---------------+  +---------------+  |\n+----------------------------------------+\n|               Analytics & Reporting    |\n|  +---------------+  +---------------+  |\n|  |  BI           |  |   Real-time    |  |\n|  |  (Tableau)    |  |   Analytics    |  |\n|  +---------------+  +---------------+  |\n+----------------------------------------+\n|               Customer Support & CRM   |\n|  +---------------+  +---------------+  |\n|  |  CRM          |  |   Live Chat    |  |\n|  |  (Salesforce) |  |   (Intercom)   |  |\n|  +---------------+  +---------------+  |\n+----------------------------------------+\n```\n\n### Conclusion\nThis architecture ensures that the e-commerce platform is scalable, secure, and performant. By leveraging microservices, cloud infrastructure, and modern DevOps practices, the platform can handle high traffic, provide a seamless user experience, and adapt to changing business needs."
}

@app.post("/get_json_v1")
def get_json_v1(model: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE, system_message: Optional[str] = None):
    session_id = str(len(sessions) + 1)
    sessions[session_id] = ChatSession(model, temperature, system_message)
    return {"nodes":[{"id":"users","label":"User","textDimension":{"width":33,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-route-53","label":"Route53","textDimension":{"width":59,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-cloudfront","label":"CloudFront","textDimension":{"width":77,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-elastic-load-balancing","label":"ELB","textDimension":{"width":31,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-ec2","label":"EC2","textDimension":{"width":32,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-rds","label":"RDS","textDimension":{"width":34,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-s3-on-outposts","label":"S3","textDimension":{"width":20,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-lambda","label":"Lambda","textDimension":{"width":58,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-api-gateway","label":"APIGateway","textDimension":{"width":86,"height":20},"nodeDimension":{"width":100,"height":100}},{"id":"aws-simple-queue-service","label":"SNS/SQS","textDimension":{"width":71,"height":20},"nodeDimension":{"width":100,"height":100}}],"edges":[{"id":"User_Route53","from":"users","to":"aws-route-53"},{"id":"Route53_CloudFront","from":"aws-route-53","to":"aws-cloudfront"},{"id":"CloudFront_S3","from":"aws-cloudfront","to":"aws-s3-on-outposts"},{"id":"CloudFront_ELB","from":"aws-cloudfront","to":"aws-elastic-load-balancing"},{"id":"ELB_EC2","from":"aws-elastic-load-balancing","to":"aws-ec2"},{"id":"EC2_RDS","from":"aws-ec2","to":"aws-rds"},{"id":"EC2_APIGateway","from":"aws-ec2","to":"aws-api-gateway"},{"id":"APIGateway_Lambda","from":"aws-api-gateway","to":"aws-lambda"},{"id":"Lambda_SNS_SQS","from":"aws-lambda","to":"aws-simple-queue-service"},{"id":"RDS_EC2","from":"aws-rds","to":"aws-ec2"},{"id":"SNS_SQS_EC2","from":"aws-simple-queue-service","to":"aws-ec2"}],"group":{"vpc":{"label":"VPC","elements":["aws-route-53","aws-ec2"]},"backend":{"label":"BussinessLogic","elements":["aws-lambda","aws-ec2"]}}}

# Entry point for running the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
