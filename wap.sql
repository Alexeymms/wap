-- wap: A minimalistic wireless billing system

-- Copyright (c) 2013, 2014 Daniel Corbe
-- All rights reserved.

-- Permission is hereby granted, free of charge, to any person obtaining a
-- copy of this software and associated documentation files (the
-- "Software"), to deal in the Software without restriction, including
-- without limitation the rights to use, copy, modify, merge, publish,
-- distribute, sublicense, and/or sell copies of the Software, and to
-- permit persons to whom the Software is furnished to do so, subject to
-- the following conditions:

-- 1. Redistributions of source code must retain the above copyright
--    notice, this list of conditions and the following disclaimer.
-- 2. Redistributions in binary form must reproduce the above copyright
--    notice, this list of conditions and the following disclaimer in the
--    documentation and/or other materials provided with the distribution.
-- 3. Neither the name of the authors, copyright holders or the contributors
--    may be used to endorese or promote products derived from this software
--    without specific prior written permission.

-- THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS, AUTHORS AND
-- CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
-- BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
-- FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL
-- THE COPYRIGHT HOLDERS, AUTHORS OR CONTRIBUTORS BE HELD LIABLE FOR ANY
-- DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
-- DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
-- GOODS OR SERVICES; LOSS OF USE, DATA, COPYRIGHT ENFRINGEMENT, LOSS
-- OF PROFITS, REVENUE, OR BUSINESS INTERRUPTION) HOWEVER CAUSED
-- AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY
-- OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
-- OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
-- SUCH DAMAGE.

CREATE TABLE `cards` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `card` char(18) NOT NULL,
  `balance` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `i_product` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card` (`card`)
) ENGINE=InnoDB;

CREATE TABLE `ledger` (
  `i_user` bigint(20) unsigned NOT NULL DEFAULT '0',
  `i_card` bigint(20) unsigned NOT NULL DEFAULT '0',
  `type` enum('Credit','Debit','Activation') NOT NULL,
  `amount` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `reason` varchar(256) NOT NULL,
  `i_agent` bigint(20) unsigned NOT NULL DEFAULT '1',
  `session` varchar(64) DEFAULT NULL,
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY `session` (`session`)
) ENGINE=InnoDB;

CREATE TABLE `products` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `price` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `activation` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `fee` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `day` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(64) NOT NULL,
  `email` varchar(128) NOT NULL,
  `phone` varchar(16) DEFAULT NULL,
  `balance` decimal(10,6) NOT NULL DEFAULT '0.000000',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `email` (`email`)
) ENGINE=InnoDB;

CREATE TABLE `nas` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `identifier` char(30) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `identifier` (`identifier`)
) ENGINE=InnoDB;

CREATE TABLE `nas_options` (
  `id` bigint(20) unsigned NOT NULL,
  `attribute` char(30) NOT NULL,
  `value` char(128) NOT NULL,
  PRIMARY KEY (`id`,`attribute`)
) ENGINE=InnoDB;

CREATE TABLE `user_options` (
  `id` bigint(20) unsigned NOT NULL,
  `attribute` char(30) NOT NULL,
  `value` char(128) NOT NULL,
  PRIMARY KEY (`id`,`attribute`)
) ENGINE=InnoDB;

CREATE TABLE `card_options` (
  `id` bigint(20) unsigned NOT NULL,
  `attribute` char(30) NOT NULL,
  `value` char(128) NOT NULL,
  PRIMARY KEY (`id`,`attribute`)
) ENGINE=InnoDB;
