-- wap: A minimalistic wireless billing system

-- Copyright(C) 2013 Global Reach Communications, Inc.
-- All Rights Reserved.

-- You have obtained a development version of this software in its source format.
-- You may not modify, redistribute or re-use this software under any circumstances,
-- including (but not limited to): selling, sublicensing, transferring owership,
-- creating derivative works, copying or reinstalling.  For more information, please
-- contact licensing@globalreachcomm.com

CREATE TABLE `cards` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `card` char(18) NOT NULL,
  `balance` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `i_product` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `card` (`card`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1

CREATE TABLE `products` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `description` varchar(256) DEFAULT NULL,
  `price` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `activation` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `fee` decimal(10,6) NOT NULL DEFAULT '0.000000',
  `day` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1
