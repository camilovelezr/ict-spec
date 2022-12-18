# Interoperable Analysis Plugin

This document defines an Interoperable Analysis Plugin (IAP). The goal of this document is to enable the creation and dissemination of interoperable tools for image analysis, molecular modeling, genomics, bioinformatics, or any other scientific domain.

## Table of Contents

- [Overview](#overview)
- [Tool Packaging](#tool-packaging)
- [Metadata](#metadata)
- [Inputs and Outputs](#inputs-and-outputs)
- [User Interface](#user-interface)
- [Hardware Requirements](#hardware-requirements)

## Notational Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" are to be interpreted as described in [RFC 2119](https://tools.ietf.org/html/rfc2119).

## Definitions

Unless specified otherwise in the documentation, all usage of the words/phrases listed [here](definitions.md) are explicitly defined in manner which MAY or MAY NOT adhere to conventional or colloquial definitions.

# Overview

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
  description: Input image collection to be processed by this plugin
  type: path
  format: 
    uri: http://edamontology.org/format_3727
    term: OME-TIFF
- name: thresholdtype
  required: true
  description: Algorithm type for thresholding
  type: string
  format:
    uri: http://edamontology.org/operation_image_thresholding
    term: plain text format
- name: thresholdvalue
  required: false
  description: Threshold value for manual setting
  type: number
  format: 
    uri:
    term:
outputs:
- name: output
  required: true
  description: Output data for the plugin
  type: path
  format: [image thresholding]
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

# Tool Packaging

Each tool MUST be packaged as container image and hosted on a public or private image repository. The container MUST adhere to the [OCI Image Format](https://github.com/opencontainers/image-spec) and can be built using a number of different container engines, including (but not limited to): [Docker](https://www.docker.com/) and [Podman](https://podman.io/). Each container image MUST contain all necessary dependencies required to run the analysis code contained within, including both manually added binaries/source code and dependencies installed by package managers during the container build process. 

In order to maintain interoperability when consuming IAPs, there are several packaging requirements that each tool MUST follow:

* All packaged tools should contain an entrypoint file, which serves to provide a standard point of entry to access and run analysis code. This entrypoint MUST be a shell script (`.sh`) that MUST sit in the root of the container image (`/entrypoint.sh`). This shell script SHOULD accept command line arguments and pass them appropriately to the analysis code bundled within the tool -- a reusable example is shown [here](example/entrypoint.sh).
* References to file and directory paths within the container build instructions (ie. a Dockerfile) SHOULD use absolute paths and SHOULD NOT rely on changes to the working directory. For example, when building a container image using a Dockerfile, avoid using the `WORKDIR` instruction set to change the working directory to simplify relative path references.

# Metadata

| Field | Description | Example |
| ----- | ----------- | ------: |
| specVersion | Version of IAP specification yaml schema | 0.1.0 |
| name | Unique identifier for IAP tool scoped on organization or user, should take the format `<organization/user>/<IAP name>` | wipp/threshold | 
| version | Version of IAP, [semantic versioning](https://semver.org/) is recommended | 1.1.1 |
| container | Direct link to hosted IAP container image, should take the format `<registry path>/<image repository>:<tag>`, registry path may be omitted and will default to Docker Hub | wipp/wipp-thresh-plugin:1.1.1 |
| title | (optional) Descriptive human-readable name, will default to `name` if omitted | Thresholding Plugin |
| description | (optional) Brief description of plugin | Thresholding methods from ImageJ |
| author | Comma separated list of authors, each author name should take the format `<first name> <last name>`| Mohammed Ouladi |
| contact | Email or link to point of contact (ie. GitHub user page) for questions or issues | mohammed.ouladi@labshare.org |
| repository | Url for public or private repository hosting source code | https://github.com/polusai/polus-plugins
| documentation | (optional) Url for hosted documentation about using or modifying the plugin | 
| citation | (optional) DOI link to relavent citation, plugin users should use this citation when using this plugin | 
<br>

# Inputs and Outputs

The inputs and outputs section of the IAP specification clearly defines all possible parameters available to configure on the IAP tool. These convey parameters passed directly to the IAP tool and SHOULD dictate exactly what the IAP tool is expecting.
<br><br>
| Field | Description | Example |
| ----- | ----------- | ------: |
| name | Unique input or output name for this plugin, case-sensitive match to corresponding variable expected by tool | thresholdtype |
| required | Boolean (true/false) value indicating whether this field needs an associated value | true |
| description | Short text description of expected value for field | Algorithm type for thresholding |
| type | Defines the parameter passed to the IAP tool based on broad categories of [basic types](#types-and-formats) | string |
| format | Defines the actual value(s) that the input/output parameter represents using an [ontology schema](#ontology) | ['image thresholding'] |
<br>

## Types and Formats

The basic types broadly categorize the format of the parameter passed to the IAP tool. Each parameter is passed to the IAP tool as a command line argument and the basic types represent the format of those arguments.
<br><br>
| Type | Description | Example |
| ---- | ----------- | ------: |
| string | The most basic parameter type, effectively any set of characters | IJDefault |
| number | Any numeric characters, with no distinction between integers and floats | 2.0 |
| array | List of arbitrary string values using the convention of comma-separated values between square brackets | [1, next, 'and,2'] | 
| boolean | Limited to `true` and `false` values | true |
| path | String value that represents a file or directory path using Unix conventions | path/to/file/or/directory | 
<br>

The format defined by the `type` MAY be different from the representative format defined in the `format` field. For example, a tool may expect a JPEG image as an input. The tool is not configured, however, to accept a JPEG binary directly as a command line parameter, instead, the tool expects the input parameter to reference a file path to a JPEG image. In this case, the `type` of this input is `path`, while the `format` is `JPEG`. Appropriately defined `format` fields are used to ensure interoperability and findability for the IAP. When chaining two plugins together in sequence, the outputs of one plugin may be safely passed to the inputs of the second plugin based on matching or corresponding `format` fields. This functionality is not explicitly a part of the IAP and instead relies on the implementation and validation handled by IAP consumers -- user interface applications. The `format` field also relies heavily on a common [ontology](#ontology) -- a set of concepts and categories within a domain with explicitly defined properties and relationships to other items within the set. While the IAP is heavily reliant on a consistent and comprehensive ontology, the maintenance of such an ontology is NOT within the scope of the IAP. 

## Ontology

A comprehensive ontology plays a vital role in ensuring interoperability between IAPs. In order to safely pass parameters between IAPs in a workflow, or across workflows, the `format` field needs to draw from a predefined dictionary of terms and naming conventions. This dictionary serves as the source of truth and a reference for defining relationships, understanding context, and validating interoperability. The IAP specification relies on an open source ontology of bioscientific data analysis and data management, [EDAM](http://edamontology.org/). The EDAM ontology is well-established especially in regards to computational biology and genomics/proteomics bioinformatics concepts. The ontology is also easily extensible and significant progress has been made with the [EDAM-bioimaging](https://github.com/edamontology/edam-bioimaging), focused on adding bioimage analysis, informatics, and topics to the ontology.

When defining the `format` fields in an IAP, there are a number of conditions and caveats to keep in mind. Inputs and outputs can be loosely categorized as data and metadata. Data parameters typically fit nicely into a specific file format, for example for image data, common formats include: PNG, JPEG, TIF. These formats define how information within a file is encoded and may also define syntax within that file. Well defined data parameters are essential for enabling interoperability between plugins and should be selected with care. When defining the `format` of a data parameter, is it useful to think of the functionality embedded within the plugin tool. For example, with output parameters, what is the format of the file that the plugin tool is writing. Input data parameters can be more complex, as depending on the functionality of the plugin tool, multiple formats may be accepted. For example, a plugin tool could accept similar file formats that represent the same data (ie. CSV and Parquet) or handle format conversion as the first step within the plugin. 

Metadata parameters are usually more ambiguous and are often not sufficiently defined by a file format. Many metadata input parameters define settings or configuration values for a plugin, either as a simple numerical or string value or a more complex text file. In cases where a file format can be applied to a metadata parameter, such as JSON or YAML format text file, the file format gives little context or information about the metadata parameter. In most cases, the `format` field for metadata parameters is better served by context or semantic based ontology definitions rather than strict formats. Take the image thresholding plugin [specification](#example) for example. The input parameter `thresholdingtype` enables the user to select from a list of different thresholding algorithms. Strictly using file format for the `format` field for the `thresholdingtype` would provide no context and offers no support for interoperability. A more effective and useful definition from our ontology would be `image thresholding`, which connotes the operation being modified by this input parameter. These context based ontology definitions in the `format` field of the IAP specification can enable interoperability between plugins in a more limited or situation-specific capability. Settings and configuration style parameters are more commonly used as manual user input, rather than direct output from a previous plugin. These metadata parameters, however, play an important role in the findability of plugins, allowing users to rely on the same comprehensive ontology to categorize and filter across a list of relevant plugins. 

# User Interface

Each input and output parameter defined in the IAP specifications MUST have a corresponding user interface (UI) configuration in the `ui` section of the specification file. This UI configuration will provide meaningful guidelines and standards for any specific UI application or platform that works with or uses IAPs. The standardization provided by the UI configuration section enables portability of the IAP across different organizations, institutes, or facilities. Any UI implementation can use IAPs given that they follow a loose set of guidelines, specifically related to [basic UI types](#basic-ui-types) and handling [conditionals](#conditionals).
<br><br>
| Field | Description | Example |
| ----- | ----------- | ------- |
| key | Unique identifier to connect UI configuration to specific parameter, should take the form `<inputs or outputs>.<parameter name>` | inputs.thresholdvalue |
| title | User friendly label used in UI | "Thresholding Value" |
| description | Short user friendly instructions for selecting appropriate parameter | "Enter a threshold value" |
| type | Defines the expected user interface based on a set of [basic UI types](#basic-ui-types) | number |
| condition | [Conditional statement](#conditionals) that resolves to a boolean value based on UI configuration and selected value, used to dictate relationship between parameters | "inputs.thresholdtype=='Manual'" |
| options | Basic UI type specific options | 
<br>

## Basic UI Types

The basic UI types define a set of interactive controls that enable users to control and configure IAP parameters. To enable compatibility across different applications and platforms the UI configurations of the IAP specification need to adhere to a standard set of basic UI types. The basic types cover most generic use cases across a broad range of input and output parameters. While any particular UI application is free to implement each type as they see fit, all applications and platforms that use IAPs MUST support each of the basic UI types. By dictating the control types and options, but not any implemention details, each UI application has degree of flexibility to implement UI that adheres to the IAP requirements without sacrificing client requirements or platform integrations. This also reduces the burden and amount of work for existing UI applications solutions to integrate with the IAP specification. The `path` type best highlights the utility of this flexibility across UI implementations. Taken at face value, the `path` type is simply a formatted string and in simple applications, can be implemented as a basic text input box. An integrated platform solution, on the other hand, may have all relevant files or data stored in aggregated and cataloged data lake. This implementation of the `path` type can be much complex, allowing users to find relevant files or data using metadata based filters, searches, and autocomplete functionalities. Finally, a desktop application designed for local execution may choose to implement the `path` type using a local file browser for files or data stored on the client machine.
<br><br>
| Type | Description | Options |
| ---- | ----------- | ------- |
| text | Any arbitrary length string | `default`: prefilled value <br> `regex`: regular expression for validation <br> `toolbar`: boolean value to add text formatting toolbar | 
| number | Any numerical value | `default`: prefilled value <br> `integer`: boolean value to force integers only <br> `range`: minimum and maximum range as a tuple |
| select | Single string value from a set of options | `fields`: required array of options <br> `optional`: leave blank by default |
| multiselect | One or more string values from a set of options | `fields`: required array of options <br> `optional` leave blank by default <br> `limit`: maximum number of selections |
| color | Color values passed as RGB color values | `fields`: array of preset RGB selections |
| datetime | Standardized date and time values | `format`: datetime format using [W3C conventions](https://www.w3.org/TR/NOTE-datetime) |
| path | Absolute or relative path to file/directory using Unix conventions | `ext`: array of allowed file extensions |
| file | User uploaded binary data | `ext`: array of allowed file extensions <br> `limit`: maximum number of uploaded files <br> `size`: total file size limit
<br>

## Conditionals

Given the complexity that an IAP with several input and output parameters can introduce, it is useful to have some way to configure logical relationships in the UI flow. The `condition` field in the UI configuration enables the IAP to dictate relationships between input/output parameters and simplify the user experience for consumers of the IAP. Commonly, certain input parameters are only valid given specific configurations of other input parameters. For example, in the IAP defined above the `thresholdvalue` input parameter only applies when a specific `thresholdtype` is selected. 

## Custom UI Types





# Hardware Requirements