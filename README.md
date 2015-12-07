![Build Status](https://travis-ci.org/geowatch/geowatch-util.png)

GeoWatch Util (geowatch-util)
================

## Description

Utility library for GeoWatch, a spatially-enabled distributed message broker.

## Installation

### AWS

### Apache Kafka

For using Apache Kafka, you'll need to do something similar to the following:

```
apt-get update
apt-get install -y curl vim git
apt-get install -y zookeeperd
```

and then:

```
cd ~
wget 'http://apache.cs.utah.edu/kafka/0.8.2.0/kafka_2.10-0.8.2.0.tgz' -O 'kafka_2.10-0.8.2.0.tgz'
tar -xzvf kafka_2.10-0.8.2.0.tgz
cd kafka_2.10-0.8.2.0
# Change zookeeper port to 8002
# vim config/zookeeper.properties
# vim config/server.properties
```

## Usage

### Apache Kafka

If you are using Apache Kafka as a channel, the following might be helpful.  Set up topics, such as the following, with:

```
# Set up topics
bin/kafka-topics.sh --create --zookeeper localhost:8002 --replication-factor 1 --partitions 1 --topic requests
bin/kafka-topics.sh --create --zookeeper localhost:8002 --replication-factor 1 --partitions 1 --topic writeback
bin/kafka-topics.sh --create --zookeeper localhost:8002 --replication-factor 1 --partitions 1 --topic statistics
```


Test that GeoWatch is pushing messages properly into the Kafka channel with:

```
# Listen to topics
bin/kafka-console-consumer.sh --zookeeper localhost:8002 --topic requests --from-beginning
```

### AWS Kinesis

TBD


### AWS SNS

TBD

### AWS SQS

TBD

### Slack

TBD

## Contributing

We are currently accepting pull requests for this repository. Please provide a human-readable description with a pull request and update the README.md file as needed.

## License

Copyright (c) 2015, Patrick Dufour
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of geonode-fabric nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
