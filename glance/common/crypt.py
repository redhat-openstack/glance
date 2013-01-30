#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Routines for URL-safe encrypting/decrypting
"""

import base64
import os
import random
import string

from Crypto.Cipher import AES


def urlsafe_encrypt(key, plaintext, blocksize=16):
    """
    Encrypts plaintext. Resulting ciphertext will contain URL-safe characters
    :param key: AES secret key
    :param plaintext: Input text to be encrypted
    :param blocksize: Non-zero integer multiple of AES blocksize in bytes (16)

    :returns : Resulting ciphertext
    """
    def pad(text):
        """
        Pads text to be encrypted
        """
        pad_length = (blocksize - len(text) % blocksize)
        pad = "".join([random.choice([chr(i) for i in range(1,0xFF)])
                      for j in xrange(pad_length - 1)])
        # We use chr(0) as a delimiter between text and padding
        return text + chr(0) + pad

    # random initial 16 bytes for CBC
    init_vector = os.urandom(16)
    cypher = AES.new(key, AES.MODE_CBC, init_vector)
    padded = cypher.encrypt(pad(str(plaintext)))
    return base64.urlsafe_b64encode(init_vector + padded)


def urlsafe_decrypt(key, ciphertext):
    """
    Decrypts URL-safe base64 encoded ciphertext
    :param key: AES secret key
    :param ciphertext: The encrypted text to decrypt

    :returns : Resulting plaintext
    """
    # Cast from unicode
    ciphertext = base64.urlsafe_b64decode(str(ciphertext))
    cypher = AES.new(key, AES.MODE_CBC, ciphertext[:16])
    padded = cypher.decrypt(ciphertext[16:])
    return padded[:padded.rfind(chr(0))]
