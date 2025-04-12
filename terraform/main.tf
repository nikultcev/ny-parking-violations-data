provider "google" {
  credentials = "../secrets/gcp_credentials.json"
  project     = var.google_project
  region      = var.google_region
}
resource "google_storage_bucket" "raw-data-bucket" {
  name          = var.google_cloud_storage_bucket
  location      = var.google_cloud_storage_location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "Delete"
    }
  }
}

resource "google_bigquery_dataset" "raw" {
  dataset_id                  = "raw"
  location                    = var.google_cloud_storage_location
  default_table_expiration_ms = 86400000

  labels = {
    env = "default"
  }
}

resource "google_bigquery_dataset" "staging" {
  dataset_id                  = "staging"
  location                    = var.google_cloud_storage_location
  default_table_expiration_ms = 86400000

  labels = {
    env = "default"
  }
}

resource "google_bigquery_dataset" "report" {
  dataset_id                  = "report"
  location                    = var.google_cloud_storage_location
  default_table_expiration_ms = 86400000

  labels = {
    env = "default"
  }
}

resource "google_bigquery_table" "violations" {
  dataset_id = google_bigquery_dataset.raw.dataset_id
  table_id   = "violations"

  deletion_protection = false

  time_partitioning {
    type = "DAY"
    field = "issue_date"
  }

  clustering = [ "dataset_year","violation_code","street_name","violation_precinct" ]

  schema = <<EOF
  [
    {
      "name": "dataset_year",
      "type": "INT64"
    },
    {
      "name": "summons_number",
      "type": "INT64"
    },
    {
      "name": "plate_id",
      "type": "STRING"
    },
    {
      "name": "registration",
      "type": "STRING"
    },
    {
      "name": "plate_type",
      "type": "STRING"
    },
    {
      "name": "issue_date",
      "type": "DATE"
    },
    {
      "name": "violation_code",
      "type": "INT64"
    },
    {
      "name": "vehicle_body_type",
      "type": "STRING"
    },
    {
      "name": "vehicle_make",
      "type": "STRING"
    },
    {
      "name": "issuing_agency",
      "type": "STRING"
    },
    {
      "name": "street_code1",
      "type": "INT64"
    },
    {
      "name": "street_code2",
      "type": "INT64"
    },
    {
      "name": "street_code3",
      "type": "INT64"
    },
    {
      "name": "vehicle_expiration_date",
      "type": "DATE"
    },
    {
      "name": "violation_location",
      "type": "INT64"
    },
    {
      "name": "violation_precinct",
      "type": "INT64"
    },
    {
      "name": "issuer_precinct",
      "type": "INT64"
    },
    {
      "name": "issuer_code",
      "type": "INT64"
    },
    {
      "name": "issuer_command",
      "type": "STRING"
    },
    {
      "name": "issuer_squad",
      "type": "STRING"
    },
    {
      "name": "violation_time",
      "type": "DATETIME"
    },
    {
      "name": "time_first_observed",
      "type": "DATETIME"
    },
    {
      "name": "violation_county",
      "type": "STRING"
    },
    {
      "name": "is_violation_in_front",
      "type": "BOOL"
    },
    {
      "name": "house_number",
      "type": "STRING"
    },
    {
      "name": "street_name",
      "type": "STRING"
    },
    {
      "name": "intersecting_street",
      "type": "STRING"
    },
    {
      "name": "date_first_observed",
      "type": "DATE"
    },
    {
      "name": "law_section",
      "type": "INT64"
    },
    {
      "name": "sub_division",
      "type": "STRING"
    },
    {
      "name": "violation_legal_code",
      "type": "STRING"
    },
    {
      "name": "days_parking_in_effect",
      "type": "STRING"
    },
    {
      "name": "from_hours_in_effect",
      "type": "STRING"
    },
    {
      "name": "to_hours_in_effect",
      "type": "STRING"
    },
    {
      "name": "vehicle_color",
      "type": "STRING"
    },
    {
      "name": "is_vehicle_unregistered",
      "type": "BOOL"
    },
    {
      "name": "vehicle_year",
      "type": "INT64"
    },
    {
      "name": "meter_number",
      "type": "STRING"
    },
    {
      "name": "feet_from_curb",
      "type": "INT64"
    },
    {
      "name": "violation_post_code",
      "type": "STRING"
    },
    {
      "name": "violation_description",
      "type": "STRING"
    },
    {
      "name": "no_standing_or_stopping_violation",
      "type": "STRING"
    },
    {
      "name": "hydrant_violation",
      "type": "STRING"
    },
    {
      "name": "double_parking_violation",
      "type": "STRING"
    }
  ]
  EOF
}
