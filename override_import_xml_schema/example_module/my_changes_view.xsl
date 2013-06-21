<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rng="http://relaxng.org/ns/structure/1.0"
    >
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>
  <!-- we allow an attribute col in pages, copy the contents /-->
  <xsl:template match="rng:element[@name='page']">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
      <rng:optional><rng:attribute name="col"/></rng:optional>
    </xsl:copy>
  </xsl:template>
</xsl:stylesheet>
