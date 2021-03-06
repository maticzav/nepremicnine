import puppeteer from 'puppeteer'
import * as fs from 'fs'
import * as path from 'path'

/* Nastavitve */

const CREDS = {
  username: 'polnibizi419',
  password: 'bizi419',
}

const OUT_DIR = path.resolve(__dirname, '../../podatki/bizi/tabele.json')

// value="02" > 2
// value="03" > 3
// value="04" > 5
// value="05" > 10
// value="06" > 20
// value="07" > 50
// value="08" > 100
// value="09" > 150
// value="10" > 200
// value="11" > 250
// value="12" > 500
const ZAPOSLENI = '05'

/* Struktura podatkov */

let tabele: string[] = []

/* Zbiralec podatkov */
;(async () => {
  const browser = await puppeteer.launch({
    // executablePath: 'google-chrome-stable',
    headless: false,
    // args: [
    //   // Required for Docker version of Puppeteer
    //   '--no-sandbox',
    //   '--disable-setuid-sandbox',
    //   // This will write shared memory files into /tmp instead of /dev/shm,
    //   // because Docker’s default for /dev/shm is 64MB
    //   '--disable-dev-shm-usage',
    // ],
  })

  const page = await browser.newPage()
  await page.goto('https://bizi.si')

  console.log('Logging in!')

  /* Login */
  await page.waitForSelector('#ctl00_LoginStatus1_PanelAnon > a')

  await page.evaluate((_) => {
    // @ts-ignore
    showLoginModal()
  })

  console.log('Typing...')

  await page.waitForSelector('.login-form')
  await page.waitForTimeout(1000)

  await page.type('#ctl00_loginBoxPopup_loginBoxAlt_tbUserName', CREDS.username)
  await page.type('#ctl00_loginBoxPopup_loginBoxAlt_tbPassword', CREDS.password)

  await page.click('#ctl00_loginBoxPopup_loginBoxAlt_btnLogin')

  console.log('Waiting...')

  console.log('Logged in!')

  /* Fill in the search parameters. */

  await page.goto('https://www.bizi.si/napredno-iskanje/')

  console.log('Searching...')

  await page.waitForSelector('#ctl00_SearchAdvanced1_btnPoisciPodjetja')

  await page.select('#ctl00_SearchAdvanced1_SteviloZaposlenihOd', ZAPOSLENI)
  await page.waitForTimeout(1000)

  await page.evaluate(() => {
    // @ts-ignore
    __doPostBack('ctl00$SearchAdvanced1$btnPoisciPodjetja', '')
  })

  console.log('Displaying results...')

  /* Find all the data */
  let pagingation = 0

  while (true) {
    /* Extract table from the page. */
    await page.waitForSelector('#divResults')
    await page.waitForTimeout(5 * 1000)

    /* Extract results */
    /* prettier-ignore */
    const table = await page.evaluate(() => document.querySelector('#divResults').outerHTML)
    tabele.push(table)

    /* Save tables to file. */
    const file = path.join(OUT_DIR)
    fs.writeFileSync(file, JSON.stringify(tabele, null, 4))

    console.log(`Saved tables....${pagingation}`)

    /* Try pressing next */
    const isLast = await page.evaluate(() => {
      let element = document.querySelector<HTMLElement>(
        'ul.numbers > li:last-child',
      ).innerText

      console.log(element, parseInt(element))

      /* Once the last element equals to a page number we are on the last page. */
      if (isNaN(parseInt(element))) {
        return false
      }
      return true
    })

    /* We reached the last page */
    if (isLast) {
      break
    }

    await page.click('ul.numbers > li:last-child')
    // Update page count.
    pagingation += 1
  }

  console.log('Loaded all data...')

  await browser.close()
})()
