# Interoperable Analysis Plugin

This document defines an Interoperable Analysis Plugin (IAP). The goal of this document is to enable the creation and dissemination of interoperable tools for image analysis, molecular modeling, genomics, bioinformatics, or any other scientific domain.

### Table of Contents

- [Notational Conventions](#notational-conventions)
- [Overview](#overview)
- [Tool Packaging](#tool-packaging)
- [Metadata](#metadata)
- [Inputs and Outputs]() [TODO]
- [User Interface]() [TODO]
- [Hardware Requirements]() [TODO]

## Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" are to be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

## Definitions

Unless specified otherwise in the documentation, all usage of the words/phrases listed [here](definitions.md) are explicitly defined in manner which MAY or MAY NOT adhere to conventional or colloquial definitions.

## Overview

An IAP refers to any analysis code packaged along with dependencies for the intent of dissemination and reusability. 

An IAP is defined by two components: the specification and the tool. The specification is a YAML file that defines all parameters and requirements for a user interface to execute a predetermined piece of analysis code. Metadata contained within this file applies common [FAIR principles](https://www.go-fair.org/fair-principles/) of interoperability and reusability to discrete pieces of analysis code. The tool is a packaged piece of analysis code, complete with any and all dependencies needed to run the code. Each IAP MUST contain both a specification file and associated tool to be considered a complete IAP tool. 

Analysis code SHALL NOT be limited to any programming language, scientific domain, or use case. The IAP specification makes no requirements on the contents or scope of the analysis code, but provides some [best practices](best_practices.md), recommendations, and tips to make the most of the IAP specification.

### Example

```yaml
specVersion: 0.1.0
name: wipp/threshold
version: 1.1.1
container: wipp/wipp-thresh-plugin:1.1.1
title: Thresholding Plugin
description: Thresholding methods from ImageJ
author: Mohammed Ouladi
repository: https://github.com/usnistgov/WIPP-thresholding-plugin
documentation: 
citation: 
hardware:
  cpu:
    type: any
    min: 100
  memory:
    min: 100M
  gpu:
    type: any
    min: 
inputs:
- name: input
  required: true
  label: Input image collection to be processed by this plugin
  type: path
- name: thresholdtype
  required: true
  label: Threshold type for this plugin
  type: string
- name: thresholdvalue
  required: false
  label: Threshold value for manual setting
  type: number
outputs:
- name: output
  required: true
  label: Output data for the plugin
  type: path
ui: 
- key: inputs.input
  title: "Image Collection: "
  description: "Pick a collection..."
  type: text
- key: inputs.thresholdtype
  title: "Threshold Type"
  description: "Pick a thresholdtype"
  type: radio
  fields: [Manual, IJDefault, Huang, Huang2, Intermodes, IsoData, Li, MaxEntropy, Mean, MinErrorI, Minimum, Moments, Otsu, Percentile, RenyiEntropy, Shanbhag, Triangle, Yen]
- key: inputs.thresholdvalue
  title: Threshold Value
  description: 
  type: number
  condition: "inputs.thresholdtype=='Manual'"
```

## Tool Packaging

Each tool MUST be packaged as container image and hosted on a public or private image repository. The container MUST adhere to the [OCI Image Format](https://github.com/opencontainers/image-spec) and can be built using a number of different container engines, including (but not limited to): [Docker](https://www.docker.com/) and [Podman](https://podman.io/). Each container image MUST contain all necessary dependencies required to run the analysis code contained within, including both manually added binaries/source code and dependencies installed by package managers during the container build process. 

In order to maintain interoperability when consuming IAPs, there are several packaging requirements that each tool MUST follow:

* All packaged tools should contain an entrypoint file, which serves to provide a standard point of entry to access and run analysis code. This entrypoint MUST be a shell script (`.sh`) that MUST sit in the root of the container image (`/entrypoint.sh`). This shell script SHOULD accept command line arguments and pass them appropriately to the analysis code bundled within the tool -- a reusable example is shown [here](example/entrypoint.sh).
* References to file and directory paths within the container build instructions (ie. a Dockerfile) SHOULD use absolute paths and SHOULD NOT rely on changes to the working directory. For example, when building a container image using a Dockerfile, avoid using the `WORKDIR` instruction set to change the working directory to simplify relative path references.

## Metadata

| Field    | Description     | Example  |
| -------- | --------------- | -------: |
| specVersion | Version of IAP specification yaml schema | 0.1.0 |
| name | Unique identifier for IAP tool scoped on organization or user, should take the format `<organization/user>/<IAP name>` | wipp/threshold | 
| version | Version of IAP, [semantic versioning](https://semver.org/) is recommended | 1.1.1 |
| container | Direct link to hosted IAP container image, should take the format `<registry path>/<image repository>:<tag>`, registry path may be omitted and will default to Docker Hub | wipp/wipp-thresh-plugin:1.1.1 |
| title | (optional) Descriptive human-readable name, will default to `name` if omitted | Thresholding Plugin |
| description | (optional) Brief description of plugin | Thresholding methods from ImageJ |
| author | 
| repository |
| documentation | (optional)
| citation | (optional)
