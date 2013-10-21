<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:rng="http://relaxng.org/ns/structure/1.0">
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
    <xsl:template match="rng:element[@name='separator']">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
            <rng:optional><rng:attribute name="options"/></rng:optional>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>
