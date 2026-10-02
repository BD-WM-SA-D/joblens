> [← Mục lục](README.md)

# Tài liệu tham khảo

## Tài liệu môn học (căn cứ chính theo R12)

- **IT4931 Big Data Storage and Processing**, SOICT – HUST: L01 Overview · L02 Hadoop ecosystem · L03 HDFS · L04 Lakehouse · L05 NoSQL · L06 DynamoDB · L07 Presto/Trino · L08 Kafka · L09 Lambda/Kappa · L10 Spark batch · L11 Spark Structured Streaming · L12 Flink internals · L13 Spark ML · **L14 Lakehouse pipeline (Project ideas)**.
- **IT3120 Phân tích thiết kế hệ thống** (GV Nguyễn Hữu Đức): l00 Course overview · l01 Introduction · l02 Business Modeling · l03 Requirement · l04 Analysis & Design · l05 Architecture · **group-project-guideline.docx**. Giáo trình trong l00: Nguyễn Văn Ba – *Phát triển hệ thống hướng đối tượng với UML 2.0 và C++* (2008); Booch – *Object-Oriented Analysis and Design with Applications*; Kruchten – *The Rational Unified Process* (3rd ed.); Gamma et al. – *Design Patterns* (1994); Dennis, Wixom, Roth – *Systems Analysis and Design* (6th ed., 2014).
- **Web Mining**: L01 Intro · L02 Machine Learning (01–03) · L03 Data visualization · L04 Information retrieval · L05 Link analysis (01–02) · L06 Opinion mining (01–03) · L07 Information extraction · L08 Recommendation systems · L09 Online ads & query mining.

## Bài báo và sách nền tảng

- Pham Dinh H., Nguyen Huy H., El-Haj M. *VietJobs: A Vietnamese Job Advertisement Dataset.* LREC 2026. [arXiv](https://arxiv.org/html/2603.05262v1) · [ACL Anthology](https://aclanthology.org/2026.lrec-1.501/)
- Zhang M. et al. *SkillSpan: Hard and Soft Skill Extraction from English Job Postings.* NAACL 2022. [link](https://www.researchgate.net/publication/362270563_SkillSpan_Hard_and_Soft_Skill_Extraction_from_English_Job_Postings)
- Nguyen D. Q., Nguyen A. T. *PhoBERT: Pre-trained language models for Vietnamese.* Findings of EMNLP 2020.
- Armbrust M. et al. *Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics.* CIDR 2021.
- Zaharia M. et al. *Resilient Distributed Datasets.* NSDI 2012 · Kreps J. et al. *Kafka: a Distributed Messaging System for Log Processing.* NetDB 2011 · Sethi R. et al. *Presto: SQL on Everything.* ICDE 2019 · DeCandia G. et al. *Dynamo.* SOSP 2007.
- Kleppmann M. *Designing Data-Intensive Applications.* O'Reilly.
- Liu B. *Web Data Mining* (2nd ed.) và *Sentiment Analysis and Opinion Mining* · Manning C., Raghavan P., Schütze H. *Introduction to Information Retrieval.*
- Page L. et al. *The PageRank Citation Ranking* (1999) · Blondel V. et al. *Fast unfolding of communities in large networks* (2008) · Koren Y., Bell R., Volinsky C. *Matrix Factorization Techniques for Recommender Systems* (2009) · He X. et al. *Neural Collaborative Filtering.* WWW 2017.
- Kruchten P. *The 4+1 View Model of Architecture.* IEEE Software 1995 · Richards M., Ford N. *Fundamentals of Software Architecture.* O'Reilly.

## Tài liệu công nghệ

[Strimzi – KRaft](https://strimzi.io/kraft/) · [Strimzi releases](https://github.com/strimzi/strimzi-kafka-operator/releases) · [Apache Spark (endoflife.date)](https://endoflife.date/apache-spark) · [Apache Iceberg 1.11](https://opensource.googleblog.com/2026/05/announcing-apache-iceberg-1110.html) · [Iceberg Kafka Connect](https://iceberg.apache.org/docs/nightly/kafka-connect/) · [Iceberg catalogs 06/2026](https://dev.to/alexmercedcoder/the-state-of-apache-iceberg-catalogs-in-june-2026-265e) · [Trino Iceberg connector](https://trino.io/docs/current/connector/iceberg.html) · [Trino on Kubernetes](https://trino.io/docs/current/installation/kubernetes.html) · [Airflow on Kubernetes](https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/kubernetes.html) · [GX Core changelog](https://docs.greatexpectations.io/docs/core/changelog/) · [dbt v2 / Fusion](https://duckdb.org/2026/09/22/dbt-fusion) · [Kubeflow Spark Operator](https://www.kubeflow.org/docs/components/spark-operator/) · [MinIO alternatives](https://blog.elest.io/rustfs-vs-seaweedfs-vs-garage-which-minio-alternative-should-you-pick/) · [bkai vietnamese-bi-encoder](https://huggingface.co/bkai-foundation-models/vietnamese-bi-encoder)

## Dataset và nguồn dữ liệu

[VietJobs (GitHub)](https://github.com/VinNLP/VietJobs) · [ESCO v1.2](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/esco-v12) · [ESCO CSV](https://esco.ec.europa.eu/en/about-esco/escopedia/escopedia/comma-separated-values-csv) · [Skill-Extraction-benchmark](https://github.com/jensjorisdecorte/Skill-Extraction-benchmark/) · [vietnamese-job-skill-ner](https://github.com/phamthaic4/vietnamese-job-skill-ner) · [Vietnamese sentiment datasets (underthesea)](https://github.com/undertheseanlp/NLP-Vietnamese-progress/blob/master/tasks/sentiment_analysis.md) · [CareerBuilder Job Recommendation](https://www.kaggle.com/competitions/job-recommendation/overview/prizes) · [TopCV robots.txt](https://www.topcv.vn/robots.txt) · [ITviec robots.txt](https://itviec.com/robots.txt)

## Pháp lý

Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 và Nghị định 356/2025/NĐ-CP – tóm tắt: [Tilleke & Gibbins](https://www.tilleke.com/insights/vietnams-new-personal-data-protection-law-a-closer-look/), [DataGuidance](https://www.dataguidance.com/news/vietnam-personal-data-protection-law-enters-force).

---

*Đây là đề xuất để nhóm thảo luận. Những chỗ ghi "đề xuất", "ước lượng" hoặc "cần kiểm chứng" phải được xác nhận bằng số đo thực tế hoặc ý kiến giảng viên trước khi đưa vào báo cáo chính thức.*
