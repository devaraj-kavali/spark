/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package org.apache.spark.resource

/**
 * An executor resource request. This is used in conjuntion with the ResourceProfile to
 * programmatically specify the resources needed for an RDD that will be applied at the
 * stage level.
 * There are alternative constructors for working with Java.
 *
 * @param resourceName Name of the resource
 * @param amount Amount requesting
 * @param units Optional units of amount for things like Memory, default is no units, only byte
 *              types (b, mb, gb, etc) are supported.
 * @param discoveryScript Optional script used to discovery the resources
 * @param vendor Optional vendor, required for some cluster managers
 *
 * This api is currently private until the rest of the pieces are in place and then it
 * will become public.
 */
class ExecutorResourceRequest(
    val resourceName: String,
    val amount: Int,
    _units: Option[String] = None,
    _discoveryScript: Option[String] = None,
    _vendor: Option[String] = None) extends Serializable {

  def this(resourceName: String, amount: Int) {
    this(resourceName, amount, None, None, None)
  }

  def this(resourceName: String, amount: Int, units: String) {
    this(resourceName, amount, if (units.isEmpty()) None else Some(units), None, None)
  }

  def this(resourceName: String, amount: Int, units: String, discoveryScript: String) {
    this(resourceName, amount, if (units.isEmpty()) None else Some(units),
      Some(discoveryScript), None)
  }

  def this(resourceName: String,
      amount: Int,
      units: String,
      discoveryScript: String,
      vendor: String) {
    this(resourceName,
      amount,
      if (units.isEmpty()) None else Some(units),
      if (discoveryScript.isEmpty()) None else Some(discoveryScript),
      if (vendor.isEmpty()) None else Some(vendor))
  }

  // API not using Option to be accessible from Java
  def units: String = _units.getOrElse("")

  def discoveryScript: String = _discoveryScript.getOrElse("")

  def vendor: String = _vendor.getOrElse("")

  override def toString(): String = {
    s"ExecutorResourceRequest: resourceName = $resourceName, amount = $amount, " +
      s"discoveryScript = $discoveryScript, vendor = $vendor"
  }
}
