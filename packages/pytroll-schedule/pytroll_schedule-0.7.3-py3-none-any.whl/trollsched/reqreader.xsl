<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
  <html>
    <link rel="stylesheet" type="text/css" href="reqreader.css" />
    <link href="http://fonts.googleapis.com/css?family=EB+Garamond" rel="stylesheet" type="text/css" />
    <link href='http://fonts.googleapis.com/css?family=Ubuntu+Mono' rel='stylesheet' type='text/css' />
    <head>
      <script LANGUAGE="JavaScript1.1">

        function changeImage(id, oname) {
        document.images[id].src = eval(oname + ".src");
        }

        function changeVisibility(id, val) {
        document.images[id].style.visibility = val;
        }

      </script>
    </head>
    <body>
      <h1>
        Pass plan <xsl:value-of select="acquisition-schedule/properties/requested-on"/>
      </h1>
      <xsl:apply-templates/>
    </body>
  </html>
</xsl:template>

<xsl:template match="acquisition-schedule">
  <table>
    <tr>
      <th>Satellite</th>
      <th>Date</th>
      <th>AOS</th>
      <th>LOS</th>
    </tr>
    <xsl:for-each select="pass">
      <xsl:element name="tr">
          <xsl:attribute name="onmouseover">changeVisibility('<xsl:value-of select="@img"/>','visible')</xsl:attribute>
          <xsl:attribute name="onmouseout">changeVisibility('<xsl:value-of select="@img"/>','hidden')</xsl:attribute>
         <xsl:if test="@rec='True'"><xsl:attribute name="style">font-weight: bold</xsl:attribute></xsl:if>
        <td>
          <xsl:value-of select="@satellite"/>
        </td>
        <td style="padding-left: 2em">
          <xsl:value-of select="substring(@start-time, 0, 11)"/>
        </td>
        <td style="padding-left: 2em">
          <xsl:value-of select="substring(@start-time, 12)"/>
        </td>
        <td style="padding-left: 2em">
          <xsl:value-of select="substring(@end-time, 12)"/>
        </td>
        <td>
          <xsl:element name="img">
            <xsl:attribute name="src"><xsl:value-of select="substring(@img, 45)"/></xsl:attribute>
            <xsl:attribute name="name"><xsl:value-of select="@img"/></xsl:attribute>
            <xsl:attribute name="style">visibility: hidden; position: fixed; top:10px; right:10px;</xsl:attribute>
          </xsl:element>
        </td>
      </xsl:element>
    </xsl:for-each>
  </table>
</xsl:template>



<xsl:template match="product">
  <li>
    <xsl:element name="label">
      <xsl:attribute name="type">label</xsl:attribute>
      <xsl:attribute name="class">folder</xsl:attribute>
      <xsl:attribute name="for"><xsl:value-of select="../@id"/><xsl:value-of select="@id"/></xsl:attribute>
      <xsl:value-of select="@id"/>
    </xsl:element>
    <xsl:element name="input">
      <xsl:attribute name="type">checkbox</xsl:attribute>
      <xsl:attribute name="class">folder</xsl:attribute>
      <xsl:attribute name="id"><xsl:value-of select="../@id"/><xsl:value-of select="@id"/></xsl:attribute>
    </xsl:element>
    <xsl:variable name="product" select="@id"/>
    <ul>
      <xsl:apply-templates />
    </ul>
  </li>
</xsl:template>


<xsl:template match="filename">
  <li>
    <span class="filename">
      <xsl:element name="input">
        <xsl:attribute name="type">text</xsl:attribute>
        <xsl:attribute name="size">64</xsl:attribute>
        <xsl:attribute name="id">
          <xsl:value-of select="."/><xsl:value-of select="../../@id"/><xsl:value-of select="../@id"/>
        </xsl:attribute>
        <xsl:attribute name="value"><xsl:value-of select="."/></xsl:attribute>
      </xsl:element>
      <span class="attributes">
        <xsl:apply-templates select="@*"/>
      </span>
    </span>
  </li>
</xsl:template>


<!-- file attributes -->
<xsl:template match="@*">
  <xsl:variable name="uid">
    <xsl:value-of select="name()"/><xsl:value-of select="generate-id(..)"/>
  </xsl:variable>

  <span class="attribute">
    <xsl:element name="label">
      <xsl:attribute name="type">label</xsl:attribute>
      <xsl:attribute name="for"><xsl:value-of select="$uid"/></xsl:attribute>
      <xsl:value-of select="name()"/>: 
    </xsl:element>

    <xsl:variable name="val" select="."/>
    <xsl:choose>
      <xsl:when test="($val='true') or ($val='false')">
        <xsl:element name="input">
          <xsl:attribute name="type">checkbox</xsl:attribute>
          <xsl:attribute name="id"><xsl:value-of select="$uid"/></xsl:attribute>
          <xsl:if test="$val='true'">
            <xsl:attribute name="checked">checked</xsl:attribute>
          </xsl:if>
        </xsl:element>
      </xsl:when>
      <xsl:otherwise>
        <xsl:element name="input">
          <xsl:attribute name="type">text</xsl:attribute>
          <xsl:attribute name="size">4</xsl:attribute>
          <xsl:attribute name="id"><xsl:value-of select="$uid"/></xsl:attribute>
          <xsl:attribute name="value"><xsl:value-of select="$val"/></xsl:attribute>
        </xsl:element>
        
      </xsl:otherwise>
    </xsl:choose>
  </span>

</xsl:template>




<xsl:template match="metadata">
  <h2>Metadata</h2>
  <xsl:for-each select="*">
    <xsl:value-of select="name()"/>: <xsl:value-of select="."/><br/>
  </xsl:for-each>
</xsl:template>

<xsl:template match="variables">
  <h2>Variables</h2>
  <ul>
    <xsl:apply-templates/>
  </ul>
</xsl:template>

<xsl:template match="path">
  <li>
    <xsl:value-of select="@id"/>: <xsl:value-of select="."/>
  </li>
</xsl:template>

</xsl:stylesheet> 
