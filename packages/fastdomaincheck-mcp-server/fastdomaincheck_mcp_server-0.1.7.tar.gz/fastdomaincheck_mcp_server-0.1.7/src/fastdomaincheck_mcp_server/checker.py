import whois
import logging
import socket # Import the socket module

# Configure logger
# Add more detailed format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_domain_availability(domain_name: str) -> str:
    """
    Check if a single domain is available, combining WHOIS and DNS lookups.

    Args:
        domain_name: The domain name to check.

    Returns:
        "available": If the domain is available for registration.
        "registered": If the domain is already registered.
        "error: <reason>": If an unrecoverable error occurred during the query.
    """
    logger.info(f"Checking domain availability for: {domain_name}")

    # === Step 1: WHOIS Query ===
    whois_indicates_registered = False # Flag if WHOIS clearly indicates registered
    whois_query_failed = False # Flag if WHOIS query failed

    try:
        logger.debug(f"Performing WHOIS query for {domain_name}...")
        # Add timeout settings to avoid long blocks
        # Note: python-whois itself doesn't directly support timeouts, but underlying libs/syscalls might
        # Increasing granularity of try-except blocks can help handle specific errors better
        domain_info = whois.whois(domain_name)
        logger.debug(f"WHOIS query result for {domain_name}: {domain_info}")

        # Check WHOIS result
        if domain_info is None or not hasattr(domain_info, 'domain_name') or not domain_info.domain_name:
            logger.info(f"WHOIS query returned no substantial info for {domain_name} (might be available).")
            # WHOIS indicates unregistered or info incomplete, rely on DNS
        elif hasattr(domain_info, 'status') and isinstance(domain_info.status, str) and 'no match' in domain_info.status.lower():
             # Some registrars explicitly return strings like "No match for domain"
             logger.info(f"WHOIS status explicitly indicates 'no match' for {domain_name} (available).")
             return "available" # Can directly determine availability
        elif hasattr(domain_info, 'status') and isinstance(domain_info.status, list) and any('redemptionperiod' in s.lower() or 'pendingdelete' in s.lower() for s in domain_info.status):
             # Special status, registered but might be released soon, still considered 'registered'
             logger.warning(f"WHOIS indicates {domain_name} is in redemption/pending delete state, considered registered for now.")
             whois_indicates_registered = True
        elif domain_info.domain_name: # If domain_name attribute exists and is not empty
            # WHOIS returned valid info, tends to indicate registered
            logger.info(f"WHOIS query returned valid info for {domain_name} (indicates registered).")
            whois_indicates_registered = True
        else:
            # Other cases, info might be incomplete
             logger.info(f"WHOIS query for {domain_name} returned ambiguous info. Relying on DNS check.")

    except whois.parser.PywhoisError as e:
        logger.warning(f"WHOIS query for {domain_name} resulted in PywhoisError (likely available, proceeding to DNS check): {e}")
        # Query parsing error, rely on DNS
    except TimeoutError: # Catch potential timeout errors
        logger.warning(f"WHOIS query for {domain_name} timed out. Proceeding to DNS check.")
        whois_query_failed = True
    except Exception as e:
        logger.error(f"WHOIS query for {domain_name} failed with an unexpected error: {e}", exc_info=True)
        whois_query_failed = True
        # WHOIS failed, must rely on DNS check

    # === Step 2: DNS Lookup (as supplement or final confirmation) ===
    try:
        logger.debug(f"Performing DNS lookup for {domain_name}...")
        # Set DNS query timeout
        socket.setdefaulttimeout(5) # Set global socket timeout to 5 seconds
        # Use getaddrinfo to get address information
        addr_info = socket.getaddrinfo(domain_name, None)
        logger.info(f"DNS lookup for {domain_name} successful (indicates registered): {addr_info}")
        # If DNS resolution succeeds, consider it registered
        return "registered"
    except socket.gaierror as e:
        # getaddrinfo error
        if e.errno == socket.EAI_NONAME:
            logger.info(f"DNS lookup for {domain_name} failed with EAI_NONAME (indicates available).")
            # If WHOIS failed or didn't clearly indicate registered, DNS EAI_NONAME confirms availability
            if whois_query_failed or not whois_indicates_registered:
                return "available"
            else:
                # WHOIS showed registered, but DNS not found, possibly config issue or recently registered
                logger.warning(f"Domain {domain_name} indicated registered by WHOIS but DNS lookup failed (EAI_NONAME). Returning registered due to WHOIS.")
                return "registered" # Prioritize WHOIS registered status
        else:
            logger.error(f"DNS lookup for {domain_name} failed with GAIError: {e}", exc_info=True)
            # If WHOIS also failed, return error
            if whois_query_failed:
                 return f"error: Both WHOIS and DNS lookups failed. DNS GAIError: {e}"
            # If WHOIS succeeded and indicated registered, return registered
            elif whois_indicates_registered:
                 logger.warning(f"DNS lookup failed for {domain_name} but WHOIS indicated registered. Returning registered.")
                 return "registered"
            # If WHOIS didn't indicate registered and DNS failed (non-EAI_NONAME), return error
            else:
                 return f"error: DNS lookup failed unexpectedly. DNS GAIError: {e}"
    except socket.timeout:
        logger.error(f"DNS lookup for {domain_name} timed out.")
        if whois_query_failed:
            return "error: Both WHOIS and DNS lookups failed (DNS timeout)."
        elif whois_indicates_registered:
            logger.warning(f"DNS lookup timed out for {domain_name} but WHOIS indicated registered. Returning registered.")
            return "registered"
        else:
            return "error: DNS lookup timed out."
    except Exception as e:
        logger.error(f"An unexpected error occurred during DNS lookup for {domain_name}: {e}", exc_info=True)
        if whois_query_failed:
            return f"error: Both WHOIS and DNS lookups failed. Unexpected DNS error: {e}"
        elif whois_indicates_registered:
            logger.warning(f"Unexpected DNS error for {domain_name} but WHOIS indicated registered. Returning registered.")
            return "registered"
        else:
            return f"error: Unexpected DNS lookup failure: {e}"
    finally:
        # Restore default timeout setting to avoid affecting other socket operations
        socket.setdefaulttimeout(None)

# (Optional) Add a function for batch checking
# Note: Current batch check is serial. Consider async or multithreading for high performance.
def check_domains_availability(domain_names: list[str]) -> dict[str, str]:
    """
    Check the availability of multiple domains in batch.

    Args:
        domain_names: A list of domain names to check.

    Returns:
        A dictionary where keys are domain names and values are their status 
        ("available", "registered", or "error: <reason>").
    """
    results = {}
    logger.info(f"Starting batch check for {len(domain_names)} domains.")
    for domain in domain_names:
        results[domain] = check_domain_availability(domain)
    logger.info("Batch check completed.")
    return results 