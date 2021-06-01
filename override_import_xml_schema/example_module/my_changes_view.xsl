<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rng="http://relaxng.org/ns/structure/1.0"
    >
  <!-- @* matches any attribute node, and node() matches any other kind of node
       (element, text node, processing instruction or comment)
  -->
  <!-- This basicaly matches everything and copies it unchanged. -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
  <!-- we allow an attribute col in pages, copy the contents /-->
  <!-- The specific match on en element with name 'page' overrides the very
       general match above.
  -->
  <xsl:template match="rng:element[@name='page']">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
      <rng:optional><rng:attribute name="col"/></rng:optional>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
