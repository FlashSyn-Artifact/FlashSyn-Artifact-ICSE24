# Use Python 3.7.5 as the base image
FROM python:3.7.5

# Set the working directory in the container
WORKDIR /FlashSyn

# Install timeout command
RUN apt-get update && apt-get install -y coreutils

# Copy the requirements.txt file into the container at /FlashSyn
COPY . /FlashSyn/

RUN pip install --upgrade pip

# Install any dependencies in the requirements.txt
RUN python3.7 -m  pip install --no-cache-dir -r requirements.txt

# install rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# update Rust
RUN . ~/.bashrc; rustup update stable

# Install foundryup
RUN rm -rf ~/.foundry/ && \
    curl -L https://foundry.paradigm.xyz | bash 

# Install Foundry CLI
RUN . ~/.bashrc; foundryup -C 6fc06c5539efb86b0204331f8a5749a60390389a

RUN . ~/.bashrc